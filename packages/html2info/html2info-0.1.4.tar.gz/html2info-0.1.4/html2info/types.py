from typing import TypedDict


class EducationType(TypedDict):
    university_name: str | None
    degree_and_major: str | None
    dates: str | None
    university_link: str | None
    image_link: str | None


class ExperienceType(TypedDict):
    title: str | None
    company: str | None
    image_link: str | None
    company_link: str | None
    dates: str | None
    description: str | None
