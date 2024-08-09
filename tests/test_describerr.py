import os.path
import subprocess

import pytest

from describerr import describerr

expected_out = describerr.Commits(
    generic={
        "feat": [
            describerr.Commit(
                raw="feat: Add feature 1. <CommitAuthor1> 000000101",
                prefix="feat",
                scope=None,
                topic="Add feature 1.",
                author="CommitAuthor1",
                breaking=False,
                hash="000000101",
            ),
            describerr.Commit(
                raw="feat(scope1): Add feature 1 but with scope1 <CommitAuthor3> 000000808",
                prefix="feat",
                scope="scope1",
                topic="Add feature 1 but with scope1",
                author="CommitAuthor3",
                breaking=False,
                hash="000000808",
            ),
            describerr.Commit(
                raw="feat: Author with many spaces and tabs              <CommitAuthor1> 000001111",
                prefix="feat",
                scope=None,
                topic="Author with many spaces and tabs",
                author="CommitAuthor1",
                breaking=False,
                hash="000001111",
            ),
            describerr.Commit(
                raw="feat: Author inside<CommitAuthor>the subject <AuthorWasInsideSubject No Spaces> 000001212",
                prefix="feat",
                scope=None,
                topic="Author inside<CommitAuthor>the subject",
                author="AuthorWasInsideSubject No Spaces",
                breaking=False,
                hash="000001212",
            ),
            describerr.Commit(
                raw="feat: Author inside <CommitAuthor> the subject separated <AuthorWasInsideSubject With Spaces> "
                "000001313",
                prefix="feat",
                scope=None,
                topic="Author inside <CommitAuthor> the subject separated",
                author="AuthorWasInsideSubject With Spaces",
                breaking=False,
                hash="000001313",
            ),
        ],
        "chore": [
            describerr.Commit(
                raw="chore: Rename files because rails where wrong <CommitAuthor1> 000000202",
                prefix="chore",
                scope=None,
                topic="Rename files because rails where wrong",
                author="CommitAuthor1",
                breaking=False,
                hash="000000202",
            ),
            describerr.Commit(
                raw="chore(scope1): Rename files because rails were wrong in scope 1 <CommitAuthor2> 000000909",
                prefix="chore",
                scope="scope1",
                topic="Rename files because rails were wrong in scope 1",
                author="CommitAuthor2",
                breaking=False,
                hash="000000909",
            ),
        ],
        "fix": [
            describerr.Commit(
                raw="fix: fixed some bugs. YEAH! <CommitAuthor1> 000000303",
                prefix="fix",
                scope=None,
                topic="Fixed some bugs. YEAH!",
                author="CommitAuthor1",
                breaking=False,
                hash="000000303",
            ),
            describerr.Commit(
                raw="fix(scope2): fixed some bugs. YEAH for scope2! <CommitAuthor1> 000000a0a",
                prefix="fix",
                scope="scope2",
                topic="Fixed some bugs. YEAH for scope2!",
                author="CommitAuthor1",
                breaking=False,
                hash="000000a0a",
            ),
        ],
        "refactor": [
            describerr.Commit(
                raw="refactor: what the tigers like <CommitAuthor2> 000000505",
                prefix="refactor",
                scope=None,
                topic="What the tigers like",
                author="CommitAuthor2",
                breaking=False,
                hash="000000505",
            ),
        ],
        "docs": [
            describerr.Commit(
                raw="docs: I don't like it.... <CommitAuthor1> 000000404",
                prefix="docs",
                scope=None,
                topic="I don't like it....",
                author="CommitAuthor1",
                breaking=False,
                hash="000000404",
            ),
            describerr.Commit(
                raw="docs(scope3): I don't like it.... scope3 <CommitAuthor1> 000000b0b",
                prefix="docs",
                scope="scope3",
                topic="I don't like it.... scope3",
                author="CommitAuthor1",
                breaking=False,
                hash="000000b0b",
            ),
        ],
        "proj": [
            describerr.Commit(
                raw="proj: Remove obsolete configuration <PM> 000001515",
                prefix="proj",
                scope=None,
                topic="Remove obsolete configuration",
                author="PM",
                breaking=False,
                hash="000001515",
            )
        ],
        "other": [
            describerr.Commit(
                raw="This commit is created to be unparsable <CommitAuthor2> 000000606",
                prefix="other",
                scope=None,
                topic="This commit is created to be unparsable",
                author="CommitAuthor2",
                breaking=False,
                hash="000000606",
            ),
            describerr.Commit(
                raw="(scope1)This commit is created to be unparsable but with scope1 <CommitAuthor3> 000000c0c",
                prefix="other",
                scope=None,
                author="CommitAuthor3",
                breaking=False,
                topic="(scope1)This commit is created to be unparsable but with scope1",
                hash="000000c0c",
            ),
            describerr.Commit(
                raw="(scope1) This commit is created to be unparsable but with scope1 separated with empty space "
                "<CommitAuthor3> 000000d0d",
                prefix="other",
                scope=None,
                author="CommitAuthor3",
                breaking=False,
                topic="(scope1) This commit is created to be unparsable but with scope1 separated with empty space",
                hash="000000d0d",
            ),
        ],
    },
    breaking={
        "chore": [
            describerr.Commit(
                raw="chore!: Rename files that BREAKS! <CommitAuthor2> 000000f0f",
                prefix="chore",
                scope=None,
                topic="Rename files that BREAKS!",
                author="CommitAuthor2",
                breaking=True,
                hash="000000f0f",
            )
        ],
        "other": [
            describerr.Commit(
                raw="!: now lets try only BREAKS! <CommitAuthor2> 000001010",
                prefix="other",
                scope=None,
                topic="Now lets try only BREAKS!",
                author="CommitAuthor2",
                breaking=True,
                hash="000001010",
            )
        ],
        "feat": [
            describerr.Commit(
                raw="feat(scope with spaces 2)!: Add feature 1 but with scope1 that BREAKS! <bot> 000000e0e",
                prefix="feat",
                scope="scope with spaces 2",
                topic="Add feature 1 but with scope1 that BREAKS!",
                author="bot",
                breaking=True,
                hash="000000e0e",
            )
        ],
    },
)


git_error = b"""fatal: ambiguous argument '0.1.0..HEAD': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'"""


def test_changelog_creation(git_log, mocker):
    mocker.patch("describerr.describerr.subprocess.run").side_effect = [
        subprocess.CompletedProcess("args", 0, b"https://github.com/owner/proj", b""),
        subprocess.CompletedProcess("args", 0, git_log, ""),
    ]
    d = describerr.Describerr()
    d.parse_commits_into_obj("", "HEAD")
    assert dict(d._commits.breaking) == expected_out.breaking
    assert dict(d._commits.generic) == expected_out.generic


def test_changelog_creation_git_error(git_log, mocker, caplog):
    mocker.patch("describerr.describerr.subprocess.run").side_effect = [
        subprocess.CompletedProcess("args", 0, b"https://github.com/owner/proj", b""),
        subprocess.CompletedProcess("args", 128, git_log, git_error),
    ]
    d = describerr.Describerr()
    with pytest.raises(SystemExit) as excinfo:
        d.parse_commits_into_obj("0.0.0", "HEAD")
    assert excinfo.value.code == 128
    assert f"Most probably tag(s) does not exist. Git error:\n{git_error.decode()}" in caplog.messages


def test_markdown_creation(mocker, tmpdir, changelog):
    mocker.patch("describerr.describerr.subprocess.run").side_effect = [
        subprocess.CompletedProcess("args", 0, b"https://github.com/owner/proj", b"")
    ]
    d = describerr.Describerr()
    d._commits = expected_out
    describerr.Describerr._CHANGELOG_FILE = os.path.join(tmpdir, "CHANGELOG.md")
    mocker.patch("describerr.describerr.Describerr._get_current_date").return_value = "06/12/2022"

    d.create_changelog("v0.1")
    with open(os.path.join(tmpdir, "CHANGELOG.md"), "r") as f:
        generated_content = f.read()
    assert generated_content == changelog
