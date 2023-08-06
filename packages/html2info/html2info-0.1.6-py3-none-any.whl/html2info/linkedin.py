from typing import Optional

from bs4 import BeautifulSoup

from html2info.types import EducationType, ExperienceType


class Person:
    def __init__(self, linkein_url: str, raw_html: str) -> None:
        self.soup = BeautifulSoup(raw_html, "html.parser")
        self.linkedin_url = linkein_url

        self.name = None
        self.title = None
        self.location = None
        self.profile_photo_link = None
        self.about = None
        self.experience: list[ExperienceType] = []
        self.education_list: list[EducationType] = []
        self.about = None

    def parse(self):
        self.name = self.soup.find("h1").text.strip()
        self.title = self.soup.find("div", class_="text-body-medium").text.strip()

        self.location = self.soup.find("span", class_="text-body-small inline t-black--light break-words").text.strip()

        profile_photo = self.soup.find("img", {"alt": self.name})
        self.profile_photo_link = profile_photo["src"] if profile_photo else None

        self.parse_about()
        self.parse_experience()
        self.parse_education()

    def find_section_by_id(self, section_name: str) -> Optional[BeautifulSoup]:
        div = self.soup.find("div", {"id": section_name})
        return None if div is None else div.find_parent("section")

    def parse_about(self):
        # Find the span containing the text
        # Find the parent container with specific class
        parent_container = self.soup.find(
            "div",
            class_="pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center",
        )

        if parent_container is None:
            return
        # Find the span containing the text within the parent container
        text_span = parent_container.find("span", class_="visually-hidden")

        # Extract the text and remove extra spaces
        self.about = text_span.text.strip()

    def parse_experience(self):
        experience_section = self.find_section_by_id("experience")
        if experience_section is None:
            return

        experience_items = experience_section.find_all("li", class_="artdeco-list__item")

        for item in experience_items:
            title = item.find("span", class_="t-bold")
            company = item.find("span", class_="t-14 t-normal")
            image_link = item.find("img")["src"] if item.find("img") else None
            company_link = item.find("a", class_="optional-action-target-wrapper")["href"]

            dates = item.find("span", {"class": "t-14 t-normal t-black--light"})

            description = item.find("div", class_="inline-show-more-text")

            self.experience += [
                {
                    "title": title.span.text.strip() if title else None,
                    "company": company.span.text.strip() if company else None,
                    "image_link": image_link.strip() if image_link else None,
                    "company_link": company_link.strip() if company_link else None,
                    "dates": dates.span.text.strip() if dates else None,
                    "description": description.span.text.strip() if description else None,
                }
            ]

    def parse_education(self):
        education_section = self.find_section_by_id("education")
        if education_section is None:
            return

        # find all the li tags within the education_div
        education_list_items = education_section.find_all("li")

        # iterate through each li tag and extract the details
        for item in education_list_items:
            # extract the university name, degree and major

            degree_and_major_tags = item.find_all("span", {"class": "t-14 t-normal"})
            if len(degree_and_major_tags) == 0:
                continue

            university_name = item.find("span", {"class": "mr1"})
            degree_and_major = degree_and_major_tags[0].span

            # extract the dates
            dates = item.find("span", {"class": "t-14 t-normal t-black--light"})

            # extract the link to the university
            university_link = item.find("a")["href"]

            # extract the link to the university logo
            image_tag = item.find("img", {"class": "ivm-view-attr__img--centered"})
            image_link = image_tag["src"] if image_tag else None

            # add the education details to the list
            self.education_list += [
                {
                    "university_name": university_name.span.text.strip() if university_name else None,
                    "degree_and_major": degree_and_major.text.strip() if degree_and_major else None,
                    "dates": dates.span.text.strip() if dates else None,
                    "university_link": university_link,
                    "image_link": image_link,
                }
            ]

    def to_dict(self):
        exclude_keys = {"soup"}
        return {key: value for key, value in self.__dict__.items() if key not in exclude_keys}
