# CSV Generator
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

A CSV generator for creating datasets e.g. for machine learning models. This has been used in the creation of my demo data for my Finance Tracker.

## Screenshots & Usage
### The output location
<img width="901" height="284" alt="csv-output" src="https://github.com/user-attachments/assets/273b5df7-e09d-49c3-a4e3-fc0f3c7321ab" /><br>
Change the output location by changing the value of DIR on line 7.

### Changing the starting date
<img width="1008" height="621" alt="csv-gen" src="https://github.com/user-attachments/assets/83fd65da-2c87-4fb3-8be6-2d981e574dc6" />
The CSV generator struggles to successfully generate a file if the startdate's datetime is not set to the end of a month. Timedelta and dateRange is advised to be kept the same value, but is not a must. Tweak these to declare the range for the data e.g. if you want a dataset ranging from 5 years, you would set the timedelta and dateRange value to 1825 (365 * 5).

<br>Max_attempts can be tweaked based on your need on how long you want it to try to generate the file.

## Installation
1. Clone the repository:
```text
git clone https://github.com/Stenberg-N/csv-generator.git
cd csv-generator
```
2. Run the file:
```text
python csv-generator.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.
