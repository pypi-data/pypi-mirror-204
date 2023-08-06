from typing import Optional, TypedDict


class EducationType(TypedDict):
    university_name: Optional[str]
    degree_and_major: Optional[str]
    dates: Optional[str]
    university_link: Optional[str]
    image_link: Optional[str]


class ExperienceType(TypedDict):
    title: Optional[str]
    company: Optional[str]
    image_link: Optional[str]
    company_link: Optional[str]
    dates: Optional[str]
    description: Optional[str]
