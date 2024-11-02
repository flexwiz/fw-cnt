### <!-- Title : A cool name for the pull request -->

#### Description

<!-- A moderate description of the feature and what it does. You can precise what is new and/or what it removes.

Any relevant information that can help the reviewers understand the goal of the PR -->

#### Jira issue

<!-- The linked Jira issue. If there is not issue, and it is a hotfix, create the issue in Jira -->

#### Scope

<!-- List the affected apps and/or packages by your changes -->

#### Breaking changes

<!-- Whether or not this pull request brings breaking changes to the codebase.

**A breaking change is a non backward compatible change that cause the app to break if the code is not correctly migrated to the version of the pull request

Mention the developer team in case of a breaking change pull request (ntdt/team)
** -->

#### How to test

<!-- Give short, but relevant and clear explanations of **what** and **how** to test you pull request. -->

#### Notes

<!-- Write any additional information that doesn't fit in the other sections, to help the reviewers, or give more context to the changes brought by the pull request. -->

#### Definition of Done - checklist

For each “Pull Request” you need to ensure that the following checklist is fully done to consider it as “Good to merge”:

- [ ] Add tests that cover your changes
- [ ] Added/modified documentation as required (such as the README.md, documentation, API refs)
- [ ] Manually tested: run impacted apps locally, build impacted packages, run related test suites and lint locally
- [ ] Make sure that your PR is reviewed by at least two developers, including the Code Owners and if the issue is a Story you also need Product Owner approval
- [ ] If your PR contains any stuff related to CI, env variable, production, deployment, infra etc.. tag a dev-ops
- [ ] If your pull request contains changes in the project's dependencies, make sure they were approved by the lead
- [ ] Acceptance criteria for each issue met
