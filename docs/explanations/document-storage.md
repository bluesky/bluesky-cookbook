# Bluesky Document Storage

## Executive Summary

For the first time in the ten-year history of the Bluesky project, the Bluesky
core developers will soon recommend a change in how data and metadata from
Bluesky documents should be stored.

In the past, each Bluesky document has been stored as an individual record in a
document database. The Bluesky document representation is well-suited to
low-latency applications like live plotting, but it is not optimized for
storage at rest. Common data analysis workloads, including batch reads or
random access, are not efficient.

Now, the new recommendation involves transforming the contents of the Bluesky
documents for storage at rest in a form that is more efficient for data access.
The implementation in development involves a change in technology from a
document database (MongoDB) to SQL (PostgreSQL or SQLite).

## Motivation for and problems with original storage

From the earliest days in 2015, the Bluesky project has recommended storing
Bluesky documents in MongoDB as the "canonical" datastore, and optionally
exporting their content in other (sometimes lossy) formats. There have been
multiple Python APIs to this underlying MongoDB storage, and more recently an
HTTP API [^1]. But the underlying storage that these APIs write to and read
from has been unchanged.

A MongoDB database was created for each beamline instrument/endstation. Within
each database, a MongoDB "collection" was created for each Bluesky document
type (`run_start`, `run_stop`, `event`, ...). Documents emitted by the RunEngine
are inserted in the collection matching their document type. The MongoDB
document storage is being used like a logfile: it captures exactly what Bluesky
emitted.

There is an appealing simplicity to this design: it is straightforward to
explain and implement. And it is optimal for "replaying" the stream of
documents after an experiment---a use case that was emphasized in the early
days. It is defensible as an initial implementation. However, it is very
non-optimal for _batch reads_ and _random access_. These are critical
shortcomings in a data store.

In order to access a portion data from MongoDB as a table or an array, we
effectively take a "transpose" of the Event documents to build a columnar
representation of the data. The implementation is fairly complex, and thus
expensive to debug and maintain. And the operation imposes a performance cost
that becomes noticeable beyond ~100 events.

## A New Approach

The data comes from Bluesky as a stream of Bluesky documents. This is ideal for
low-latency applications, such as live-plotting. But for batch read and random
access, the stream needs to be transformed into chunked arrays and tables. It would be
simpler and more efficient to do the transformation while the stream of data is
being ingested into the storage, rather than every time it is read.

The new approach involves:

1. A database of metadata and pointers to data (e.g. filepaths and URIs)
2. A database of tabular data, ingested from Bluesky Event documents

For both databases (1) and (2), we propose to begin by supporting PostgreSQL
(for horizontally-scaled facility deployments) and SQLite (for development and
lab bench deployments). These are well-established, widely-trusted
technologies, and that is a strong consideration. Other technologies may be
explored later. The next section elaborates on the choice of relational
databases over document databases.

This provides good batch read performance and random access. It also transforms
the data from a Bluesky-specific layout (Bluesky documents) into something more
generic and portable, something which existing tools can be readily work
without specialized libraries.

It will still be possible to "replay" the Bluesky documents stream from saved
data. While some non-semantic information may be lost, such as the way that
data was chunked across Event Pages, the document stream will be semantically
equivalent.

The approach uses Tiled as the application that writes to and reads from these
databases, exposing access via a secure HTTP API. (It would also be feasible
to interact with the databases via other services, or directly.)

## Moving from a Document Database to a Relational Database

Why move from a document database (MongoDB) to a relational database
(PostgreSQL or SQLite)?

Relational databases fits our problem space well. Bluesky documents are in
fact, _relational_: the documents within a Bluesky Run have references (foreign keys)
between them. The current MongoDB-based solution does nothing to enforce these;
all validation is in the application layer.

The aspect of Bluesky documents that fits document databases well is the
scientific metadata. Back in 2015, we core developers took to heart some
lessons of projects that had used SQL for this and reportedly lived to regret
it, as their metadata tables ballooned to include the union of all the metadata
fields desired by all scientist users. By using a document database, Bluesky
avoided this problem.

In the years since, both PostgreSQL and SQLite have grown first-class support
for JSON [^2]. This enables us to have the best of both worlds: strictly
defined columns and enforced data relationships, incorporating free-form JSON
scientific metadata only where it is needed.

Additionally, while SQL is mature and robust, it is also experiencing something
of a resurgence of interest at the moment, with new tooling and integrations.
For example,
[Arrow Database Connectivity](https://arrow.apache.org/adbc/current/index.html)
provides high-performance, cross-language access to tabular data in a SQL
database.

Meanwhile, the case for MongoDB has grown weaker in some ways. After Bluesky's
adoption, MongoDB unfortunately changed it license to a non-open-source
license. Some core features, including point-in-time backup/restore, are
pay-walled.

Finally, SQLite may unlock many interesting use cases, as a self-contained
artifact. MongoDB has nothing comparable; while there are various attempts at
something similar, none of them can touch the ubiquity or trusted robustness of
SQLite.

## Approaching to the transition

We core developers have not ever changed the recommended Bluesky document
format, and we are approaching this transition with caution.

At a high level, our approach will be:

1. Stream documents from existing storage, "replaying" the Bluesky document stream.
2. Ingest them into the new storage, just as if they were a live experiment.
3. Stream documents from the new storage and validate semantic fidelity.

Of course, it possible to test this offline and evaluate the performance and
reliability of the new approach without disrupting operations. And it is feasible
to write to both old and new for some period as a precaution.

## Readiness

As of December 2024, the new approach is being used lightly at one new NSLS-II
beamline. We do not yet recommend it for mission-critical applications (without
the direct oversight of core developers). It is however, ready for
experimentation.

We plan to migrate existing NSLS-II beamlines beginning in January 2025.
Thereafter we will choose a time to recommend other community members migrate.

[^1]: The original Databroker (now called "v0") was a custom Python interface.
      The next incarnation ("v1") was a refactor to use the PyData community
      project Intake.` Neither had any security model. The latest incarnation
      is Tiled, which adds an HTTP service, a security model, and support for
      languages other than Python (anything that can use an HTTP API).
[^2]: Of course, it was always possible to store JSON in these databases as
      strings. But now they support efficient operations for selecting,
      updating, and building indexes on nested items within a JSON structure.
