# AI usage

Orthrus Research uses AI coding assistants as engineering tools in all of its projects, chiefly
Claude Code (Anthropic) and Codex (OpenAI). They draft and revise code, tests and documentation,
run builds and checks, and help investigate behavior. This document is the organization's single
disclosure of that use. It applies to every repository under
[orthrus-research](https://github.com/orthrus-research).

## A tool, not an author

Orthrus Research is the author of what it publishes and is responsible for every line of it. An
assistant's output is a draft, the same as a generated file or an editor's refactoring, until a
maintainer has read it, understood it and accepted it.

Commit history records what changed and how it was checked. It doesn't record which tools
produced a change, so commits carry no AI attribution lines. This page discloses the use once, for
all of them.

## Verification is the bar

A change is accepted on its verification, whatever drafted it. Each repository's
`CONTRIBUTING.md` lists its gates. For example:

- **Riven:** formatting and lint, both loader builds, and golden terrain digests rendered twice to
  confirm determinism. A change that alters generated terrain updates the digests in the same
  commit and says why.
- **Cubature:** both loader builds with the full test suite.

A change that does not pass its gates does not merge, whether a person or an assistant wrote it.

## Contributors

Contributors may use AI tools on the same terms as the maintainers:

- You are the author of what you submit. Understand it well enough to explain, defend and
  maintain it.
- It meets the repository's gates like any other change.
- You have the right to submit it under the repository's license.
- Don't give an assistant material you aren't allowed to share, such as private code or
  credentials.

Pull requests are reviewed on correctness, verification and clarity, not on how they were drafted.
Disclosing AI use in a pull request is optional.

## Questions

Ask on [Discord](https://discord.gg/qCVqhXtSzR) or write to admin@orthrus.cc.
