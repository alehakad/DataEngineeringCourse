from typing import Callable
from enum import Enum

class Gender(Enum):
    male = "M"
    female = "F"

"""
- Calclute max and min age of vaccinated and unvacinated patients
- Average length of hospitalization
- Filter function to create a new file with filtered data
"""
def calculate_corona_stats(filter_function: Callable[[int, bool, Gender], bool]):
    max_age_vaccinated, min_age_vaccinated, max_age_unvaccinated, min_age_unvaccinated = 0, 100, 0, 100
    total_hospitalized = 0
    total_days_hospitalized = 0
    with open("corona.csv", "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            gender, age, ventilated, time_between_positive_and_hospitalization, length_of_hospitalization, time_between_positive_and_recovery, is_vaccinated = line.strip().split(",")
            # add row to file if filter function returns True
            if filter_function(int(age), is_vaccinated == "Y", Gender(gender)):
                with open("filtered_corona.csv", "a") as filtered_file:
                    filtered_file.write(line)
            if is_vaccinated == "Y":
                max_age_vaccinated = max(max_age_vaccinated, int(age))
                min_age_vaccinated = min(min_age_vaccinated, int(age))
            else:
                max_age_unvaccinated = max(max_age_unvaccinated, int(age))
                min_age_unvaccinated = min(min_age_unvaccinated, int(age))
            
            total_hospitalized += 1
            total_days_hospitalized += int(length_of_hospitalization)

        print(f"Max age of vaccinated: {max_age_vaccinated}")
        print(f"Min age of vaccinated: {min_age_vaccinated}")
        print(f"Max age of unvaccinated: {max_age_unvaccinated}")
        print(f"Min age of unvaccinated: {min_age_unvaccinated}")
        print(f"Average length of hospitalization: {total_days_hospitalized/total_hospitalized}")

def create_filter_function(min_age:int, max_age:int, is_vaccinated:bool, gender:Gender):
    def filter_function(person_age:int, person_is_vaccinated:bool, person_gender: Gender):
        return person_age >= min_age and person_age <= max_age and person_is_vaccinated == is_vaccinated and person_gender == gender

    return filter_function

if __name__ == "__main__":
    filter_function = create_filter_function(32, 65, True, Gender.male)
    calculate_corona_stats(filter_function)