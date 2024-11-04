// commit-lint.config.js

// For the action commit-lint.yaml work, 
// we'll need a commit-lint configuration file (named commit-lint.config.js) in our project root. 
// This file specifies the rules for commit messages, aligning with the Conventional Commits format.

// Here’s a simple configuration for Conventional Commits
module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [2, 'always', ['feat', 'fix', 'chore', 'docs', 'style', 'refactor', 'test', 'perf']],
        'scope-empty': [2, 'never'],         // Require a scope
        'subject-case': [2, 'always', 'sentence-case'],
        'subject-min-length': [2, 'always', 10],
        'subject-max-length': [2, 'always', 50],
      },
};