const MAX_WRONG_ATTEMPTS = 3;
const LOCK_DURATION_MS = 24 * 60 * 60 * 1000;

/**
 * Creates an in-memory tracker for claim answer attempts.
 *
 * @param {() => number} now Returns the current time in milliseconds.
 */
function createClaimAttemptTracker(now = Date.now) {
  const claims = new Map();

  function getClaimState(claimId) {
    let state = claims.get(claimId);
    if (!state) {
      state = { wrongAttempts: 0, lockedUntil: null };
      claims.set(claimId, state);
    }
    return state;
  }

  function getStatus(claimId) {
    const state = getClaimState(claimId);
    const currentTime = now();

    if (state.lockedUntil !== null && currentTime >= state.lockedUntil) {
      state.wrongAttempts = 0;
      state.lockedUntil = null;
    }

    return {
      attemptsRemaining: Math.max(0, MAX_WRONG_ATTEMPTS - state.wrongAttempts),
      locked: state.lockedUntil !== null,
      lockedUntil: state.lockedUntil,
    };
  }

  return {
    /**
     * Records an answer for a claim.
     * Correct answers clear the claim's attempt history.
     *
     * @param {string} claimId Unique identifier for the claim.
     * @param {boolean} isCorrect Whether the submitted answer is correct.
     * @returns {{correct: boolean, attemptsRemaining: number, locked: boolean, lockedUntil: number|null}}
     */
    recordAttempt(claimId, isCorrect) {
      if (typeof claimId !== "string" || claimId.trim() === "") {
        throw new TypeError("claimId must be a non-empty string");
      }
      if (typeof isCorrect !== "boolean") {
        throw new TypeError("isCorrect must be a boolean");
      }

      const status = getStatus(claimId);
      if (status.locked) {
        return { correct: false, ...status };
      }

      const state = getClaimState(claimId);
      if (isCorrect) {
        state.wrongAttempts = 0;
        state.lockedUntil = null;
        return { correct: true, ...getStatus(claimId) };
      }

      state.wrongAttempts += 1;
      if (state.wrongAttempts >= MAX_WRONG_ATTEMPTS) {
        state.wrongAttempts = MAX_WRONG_ATTEMPTS;
        state.lockedUntil = now() + LOCK_DURATION_MS;
      }

      return { correct: false, ...getStatus(claimId) };
    },

    /**
     * Returns the current attempt and lock status without recording an answer.
     *
     * @param {string} claimId Unique identifier for the claim.
     */
    getStatus(claimId) {
      if (typeof claimId !== "string" || claimId.trim() === "") {
        throw new TypeError("claimId must be a non-empty string");
      }
      return getStatus(claimId);
    },
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { createClaimAttemptTracker };
}