from odmantic import ObjectId
from pydantic import BaseModel, EmailStr, Field

# Works
# Unique reference for each publication/study/work. A mongo document will exist for
# and describe  each uniquely identifed  “work”. pmid, doi (normalized),
# openalex ids are approaches to referencing such a study uniquely but any one
# of them might be used. Versioning of the publications (as in pubmed vs Nature
# vs addendums) should all be handled naturally as part of an array of
# referenced “user input documents” each with a file provided by a user (let’s
# say a pdf). How does the client software (osm cli) reliably determine this if
# two different documents could be uniquely identified differently  (pdf with
# orcid, but html or pdf variant with DOI). Is it ok to force connection to
# server to check for pre-existing records or plan for a way to link things at a
# later date?

# workflow
# Schema to describe an analysis that was run by a user. This represents
# a chain of steps that culminate in the bibliometric output json. It will
# contain the OSM invocation metadata:, “work” supplied as input, user or
# compute identifier, steps run, derivatives created


# Derivatives

# Gridfs can avoid issues with size limitations. Each derivative is an output of the
# execution of a single container with the “preceding document” or “parent”
# referenced (this could be a primary document or another derivative). A primary
# document could have several different derivatives (scibeam and rtransparent)
# and/or several versions of the same derivative type (scibeam and rtransparent
# across different releases or rtransparent or modifications of our docker
# image). A text label would be useful here but a docker image id is likely the
# sanest way to track derivatives (which would mean that all derivatives must be
# computed in a docker container).

# mriqc applies a unique id to each person so that you can aggregate and detect
# duplication.

#  Works corresponds to a single invocation of cli.
# like mriqc have a nested structure call provenance

# have collections for each metric generator, we will have many of them and they
# will reference back to the work

# One can have different views of same work (pubmedcentral and nature). Each
# would have different filenames, different provenance, different
# md5sum.

# Usually there is a final version of record, ideally we would be analysing that.
# Generally we analyse the open access pubmed central.
# We could have a notes string to provide option to include details.


class Work(BaseModel):
    id: ObjectId = Field(alias="_id")
    user_defined_id: str
    pmid: str
    doi: str
    openalex_id: str
    scopus_id: str
    file: bytes
    content_hash: str
    timestamp: str


class Derivative(BaseModel):
    id: ObjectId = Field(alias="_id")
    component_id: str
    text_label: str
    version: str


class Component(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str
    version: str
    docker_image: str
    docker_image_id: str


class Metrics(BaseModel):
    """Potentially link to other databases for extra metadata"""

    id: ObjectId = Field(alias="_id")
    metrics: dict


class Client(BaseModel):
    id: ObjectId = Field(alias="_id")
    compute_context_id: str
    email: EmailStr
    invocation_id: str


class Workflow(BaseModel):
    id: ObjectId = Field(alias="_id")
    output: Metrics
    work_id: str
    steps: list[Component]
    derivatives_created: list[Derivative]


class Invocation(BaseModel):
    """Approximate document model"""

    id: ObjectId = Field(alias="_id")
    osm_version: str
    timestamp: str
    client: Client
    work: Work
    workflow: Workflow
    output_id: str


# class Rtransparent(Component):
#     id: ObjectId = Field(alias="_id")
#     name: str = "rtransparent"
#     version: 0.13
#     docker_image: "nimh-dsst/rtransparent:0.13"
#     docker_image_id: "dsjfkldsjflkdsjlf2jkl23j"

# class ScibeamParser(Component):
#     id: ObjectId = Field(alias="_id")
#     name: str = "rtransparent"
#     version: "0.5.1"
#     docker_image: "elife/scibeam-parser:0.5.1"
#     docker_image_id: "dsjfkldsjflkdsjlf2jkl23j"
