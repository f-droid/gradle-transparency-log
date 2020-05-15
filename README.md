
# Gradle Transparency Log

This is an automated log of the gradle binaries and their checksums as
posted on:

https://gradle.org/release-checksums/

This serves as a basic [binary transparency](https://wiki.mozilla.org/Security/Binary_Transparency) append-only log for anyone to use

## API

This can also be used as a basic JSON API by getting the JSON files via the raw links:

* [all.json](https://fdroid.gitlab.io/gradle-transparency-log/all.json) - cached version of https://services.gradle.org/versions/all
* [checksums.json](https://fdroid.gitlab.io/gradle-transparency-log/checksums.json) - a simple dictionary of download URLs and matching SHA-256 checksums
* [status_codes.json](https://fdroid.gitlab.io/gradle-transparency-log/status_codes.json) - the HTTP Status Codes of the last download attempt of this process
