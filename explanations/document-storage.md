# Bluesky Document Storage

## Executive Summary

For the first time in the history of the Bluesky project, the Bluesky
core developers are recommending a change in how data and metadata
from Bluesky documents is stored at rest.

In the past, each Bluesky document has been stored as an individual record
in a NoSQL database. This is not optimal for batch reads or random access.
Our recommendation involves doing some transformation at ingestion time
to represent the data at rest in a form that is more efficient for common
data analysis workflows. The implementation in development involves a change in
technology from NoSQL (MongoDB) to SQL (PostgreSQL or SQLite).

## Motivation for and problems with original storage

From the earliest days in 2015, the Bluesky project has always recommended
storing Bluesky documents in MongoDB as the "canonical" datastore, and
optionally exporting their content in other (somewhat lossy) formats. There
have been multiple Python APIs to this underlying MongoDB storage [^1]. Now there is
also a secure HTTP API. But throughout the underlying storage that they write
to and read from has been unchanged.

A MongoDB database was created for each beamline instrument/endstation. Within
each database, a MongoDB "collection" was created for each Bluesky document
type (`run_start`, `run_stop`, `event`, ...). Documents emitted by the RunEngine
are inserted in the collection matching their document type. The MongoDB
document storage is being used like a logfile: we just write down exactly what
Bluesky emitted.

There is an appealing simplicity to this design: it is straightforward to
explain and implement. And it is optimal for "replaying" the stream of
documents after an experiment---a use case that we were originally very focused
on. It is defensible as an initial implementation. However, it is very
non-optimal for _batch reads_ and _random access_. These are critical
shortcomings in a data store.

In order to access a portion data from MongoDB as a table or an array, we
effectively take a "transpose" of the Event documents to build a columnar
representation of the data. The implementation is fairly complex, and thus
expensive to debug and maintain. And the operation imposes a performance cost
that becomes noticeable beyond ~100 events.

## New Approach

The data comes from Bluesky as a stream of Bluesky documents. This is ideal for
low-latency applications, such as live-plotting. But for batch read and random
access, the stream needs to be transformed into chunked arrays and tables. It would be
simpler and more efficient to do the transformation while the stream of data is
being ingested into the storage, rather than every time it is read.

The new approach involves:

1. A database of metadata and pointers to data (e.g. references to filepaths and URIs)
2. A database of tabular data, ingested from Bluesky Event documents

This provides good batch read performance and random access. It also transforms
the data from a Bluesky-specific layout (Bluesky documents) into something more
generic and portable, something which existing tools can be readily work
without specialized libraries.

It will still be possible to "replay" the Bluesky documents stream from saved
data. While some non-semantic information may be lost, such as the way that
data was chunked across Event Pages, the document stream will be semantically
equivalent.

The approaches uses Tiled as the application that writes to and reads from these
databases, exposing access via a secure HTTP API. (It would also be feasible
to interact with the databases via other services, or directly.)

## Moving from a Document Database to a Relational Database

Why move from a document database (MongoDB) to a relational database
(PostgreSQL or SQLite)?

## Transition

We have not ever changed the recommended Bluesky document format, and we are
approaching this transition with caution.

At a high level, our approach will be:

1. Stream documents from existing storage, "replaying" the Bluesky document stream.
2. Ingest them into the new storage, just as if they were a live experiment.
3. Stream documents from the new storage and validate semantic fidelity.

Of course, it possible to test this offline and evaluate the performance and
reliability of the new approach without disrupting operations. And it is feasible
to write to both old and new for some period as a precaution.

As of December 2024, the new approach is being used lightly at one new NSLS-II
beamline. We intend to transition an existing beamline in 

[^1]: The original Databroker (now called "v0") was a custom Python interface.
      The next incarnation ("v1") was a refactor to use the PyData community
      project Intake.` Neither had any security model. The latest incarnation
      is Tiled, which adds an HTTP service, a security model, and support for
      languages other than Python (anything that can use an HTTP API).

