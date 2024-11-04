// commit-lint.config.js

// For the action commit-lint.yaml work, 
// we'll need a commit-lint configuration file (named commit-lint.config.js) in our project root. 
// This file specifies the rules for commit messages, aligning with the Conventional Commits format.

// Here’s a simple configuration for Conventional Commits
module.exports = {
    extends: ['@commitlint/config-conventional'],
};