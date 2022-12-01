import os.path
import subprocess

from describerr import describerr

expected_out = describerr.Commits(
    generic={
        "feat": [
            describerr.Commit(
                raw="feat: Add feature 1. <CommitAuthor1>",
                prefix="feat",
                scope=None,
                topic="Add feature 1.",
                author="CommitAuthor1",
                breaking=False,
            ),
            describerr.Commit(
                raw="feat(scope1): Add feature 1 but with scope1 <CommitAuthor3>",
                prefix="feat",
                scope="scope1",
                topic="Add feature 1 but with scope1",
                author="CommitAuthor3",
                breaking=False,
            ),
            describerr.Commit(
                raw="feat: Author with many spaces and tabs              <CommitAuthor1>",
                prefix="feat",
                scope=None,
                topic="Author with many spaces and tabs",
                author="CommitAuthor1",
                breaking=False,
            ),
            describerr.Commit(
                raw="feat: Author inside<CommitAuthor>the subject <AuthorWasInsideSubject No Spaces>",
                prefix="feat",
                scope=None,
                topic="Author inside<CommitAuthor>the subject",
                author="AuthorWasInsideSubject No Spaces",
                breaking=False,
            ),
            describerr.Commit(
                raw="feat: Author inside <CommitAuthor> the subject separated <AuthorWasInsideSubject With Spaces>",
                prefix="feat",
                scope=None,
                topic="Author inside <CommitAuthor> the subject separated",
                author="AuthorWasInsideSubject With Spaces",
                breaking=False,
            ),
        ],
        "chore": [
            describerr.Commit(
                raw="chore: Rename files because rails where wrong <CommitAuthor1>",
                prefix="chore",
                scope=None,
                topic="Rename files because rails where wrong",
                author="CommitAuthor1",
                breaking=False,
            ),
            describerr.Commit(
                raw="chore(scope1): Rename files because rails were wrong in scope 1 <CommitAuthor2>",
                prefix="chore",
                scope="scope1",
                topic="Rename files because rails were wrong in scope 1",
                author="CommitAuthor2",
                breaking=False,
            ),
        ],
        "fix": [
            describerr.Commit(
                raw="fix: fixed some bugs. YEAH! <CommitAuthor1>",
                prefix="fix",
                scope=None,
                topic="Fixed some bugs. YEAH!",
                author="CommitAuthor1",
                breaking=False,
            ),
            describerr.Commit(
                raw="fix(scope2): fixed some bugs. YEAH for scope2! <CommitAuthor1>",
                prefix="fix",
                scope="scope2",
                topic="Fixed some bugs. YEAH for scope2!",
                author="CommitAuthor1",
                breaking=False,
            ),
        ],
        "refactor": [
            describerr.Commit(
                raw="refactor: what the tigers like <CommitAuthor2>",
                prefix="refactor",
                scope=None,
                topic="What the tigers like",
                author="CommitAuthor2",
                breaking=False,
            ),
        ],
        "docs": [
            describerr.Commit(
                raw="docs: I don't like it.... <CommitAuthor1>",
                prefix="docs",
                scope=None,
                topic="I don't like it....",
                author="CommitAuthor1",
                breaking=False,
            ),
            describerr.Commit(
                raw="docs(scope3): I don't like it.... scope3 <CommitAuthor1>",
                prefix="docs",
                scope="scope3",
                topic="I don't like it.... scope3",
                author="CommitAuthor1",
                breaking=False,
            ),
        ],
        "other": [
            describerr.Commit(
                raw="This commit is created to be unparsable <CommitAuthor2>",
                prefix="other",
                scope=None,
                topic="This commit is created to be unparsable",
                author="CommitAuthor2",
                breaking=False,
            ),
            describerr.Commit(
                raw="(scope1)This commit is created to be unparsable but with scope1 <CommitAuthor3>",
                prefix="other",
                scope=None,
                author="CommitAuthor3",
                breaking=False,
                topic="(scope1)This commit is created to be unparsable but with scope1",
            ),
            describerr.Commit(
                raw="(scope1) This commit is created to be unparsable but with scope1 separated with empty space "
                "<CommitAuthor3>",
                prefix="other",
                scope=None,
                author="CommitAuthor3",
                breaking=False,
                topic="(scope1) This commit is created to be unparsable but with scope1 separated with empty space",
            ),
        ],
    },
    breaking={
        "chore": [
            describerr.Commit(
                raw="chore!: Rename files that BREAKS! <CommitAuthor2>",
                prefix="chore",
                scope=None,
                topic="Rename files that BREAKS!",
                author="CommitAuthor2",
                breaking=True,
            )
        ],
        "other": [
            describerr.Commit(
                raw="!: now lets try only BREAKS! <CommitAuthor2>",
                prefix="other",
                scope=None,
                topic="Now lets try only BREAKS!",
                author="CommitAuthor2",
                breaking=True,
            )
        ],
        "feat": [
            describerr.Commit(
                raw="feat(scope with spaces 2)!: Add feature 1 but with scope1 that BREAKS! <bot>",
                prefix="feat",
                scope="scope with spaces 2",
                topic="Add feature 1 but with scope1 that BREAKS!",
                author="bot",
                breaking=True,
            )
        ],
    },
)


def test_changelog_creation(git_log, mocker):
    mocker.patch("describerr.describerr.subprocess.run").side_effect = [
        subprocess.CompletedProcess("args", 0, git_log, "")
    ]
    d = describerr.Describerr()
    d.parse_commits_into_obj("", "HEAD")
    assert dict(d._commits.breaking) == expected_out.breaking
    assert dict(d._commits.generic) == expected_out.generic


def test_markdown_creation(mocker, tmpdir, changelog):
    d = describerr.Describerr()
    d._commits = expected_out
    d._CHANGELOG_FILE = os.path.join(tmpdir, "CHANGELOG.md")

    mocker.patch("describerr.describerr.Describerr._get_current_date").return_value = "06/12/2022"

    d.create_changelog("v0.1")
    with open(os.path.join(tmpdir, "CHANGELOG.md"), "r") as f:
        generated_content = f.read()
    assert generated_content == changelog
