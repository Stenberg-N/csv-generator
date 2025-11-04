import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DIR = Path.home() / 'OneDrive' / 'Desktop'
filename = 'output.csv'
filepath = DIR / filename

expenseCategoryPool = ['Shopping', 'Bills', 'Transport', 'Health', 'Entertainment', 'Other']
incomeCategoryPool = ['Salary', 'Freelance', 'Investment']

descriptionDict = {
    'Shopping': [
        'Groceries',
        'Clothes',
        'Jewerly',
        'Skincare',
        'Tools',
        'Baking supplies'
    ],
    'Bills': [
        'Rent',
        'Internet',
        'Water bill',
        'Electricity bill',
        'Phone bill'
    ],
    'Transport': [
        'Gas',
        'Bus',
        'Taxi',
        'Rideshare',
        'Train'
    ],
    'Health': [
        'Gym membership',
        'Medication',
        'Accessories'
    ],
    'Entertainment': [
        'Movies',
        'Concert',
        'Streaming service',
        'Nightout'
    ],
    'Other': [
        'Unexpected repair',
        'Charity donation',
        'Household items',
        'Miscellaneous expense'
    ],
    'Salary': [
        'Employer paycheck'
    ],
    'Freelance': [
        'Project',
        'Invoice settlement'
    ],
    'Investment': [
        'Dividend payout'
    ]
}

amountRanges = {
    'Shopping': (10.00, 300.00),
    'Bills': (10.00, 45.00),
    'Transport': (2.00, 70.00),
    'Health': (15.00, 32.00),
    'Entertainment': (5.00, 60.00),
    'Other': (5.00, 50.00),
    'Salary': (2788.00, 3124.00),
    'Freelance': (100.00, 600.00),
    'Investment': (50.00, 400.00)
}

startDate = datetime(2025, 11, 30) - timedelta(days=1460) # Adjust the starting date here.
dateRange = 1460

dates = [startDate + timedelta(days=random.randint(0, dateRange)) for _ in range(2950)]
dates.sort()

datesByMonth = defaultdict(list)
for date in dates:
    yearMonth = date.strftime('%Y-%m')
    datesByMonth[yearMonth].append(date)

success = False
attempt = 0
max_attempts = 100

while not success and attempt < max_attempts:
    attempt += 1
    print(f"Attempt {attempt} to generate valid CSV...")

    salaryMonths = set()
    investmentMonths = set()
    healthMonths = set()
    freelanceCounts = defaultdict(int)
    entertainmentCounts = defaultdict(int)
    shoppingCounts = defaultdict(int)
    transportCounts = defaultdict(int)
    otherCounts = defaultdict(int)
    usedDates = set()

    dataRows = []

    for yearMonth, monthDates in datesByMonth.items():
        random.shuffle(monthDates)

        assignedSalary = 0
        assignedInvestment = 0
        assignedHealth = 0
        assignedShopping = 0
        assignedEntertainment = 0
        assignedTransport = 0
        assignedOther = 0

        billDescriptions = descriptionDict['Bills'].copy()
        random.shuffle(billDescriptions)
        billDates = monthDates[:len(billDescriptions)]
        if len(billDates) >= len(billDescriptions):
            for i, description in enumerate(billDescriptions):
                date = billDates[i]
                if description == 'Rent':
                    amount = 550.00
                elif description == 'Internet':
                    amount = 27.80
                else:
                    minAmount, maxAmount = amountRanges['Bills']
                    amount = round(random.uniform(minAmount, maxAmount), 2)
                dataRows.append([date.strftime('%Y-%m-%d'), 'Bills', description, amount, 'expense'])
                usedDates.add(date)
        else:
            print(f"Not enough dates in {yearMonth} for all bills")

        monthDates = [d for d in monthDates if d not in usedDates]

        for date in monthDates:
            if assignedSalary < 1:
                category = 'Salary'
                transactionType = 'income'
                salaryMonths.add(yearMonth)
                assignedSalary += 1
            elif assignedInvestment < 1:
                category = 'Investment'
                transactionType = 'income'
                investmentMonths.add(yearMonth)
                assignedInvestment += 1
            elif assignedHealth < 1 and date not in usedDates:
                category = 'Health'
                transactionType = 'expense'
                healthMonths.add(yearMonth)
                assignedHealth += 1
            elif assignedShopping < 4 and date not in usedDates:
                category = 'Shopping'
                transactionType = 'expense'
                shoppingCounts[yearMonth] += 1
                assignedShopping += 1
            elif assignedEntertainment < 2 and date not in usedDates:
                category = 'Entertainment'
                transactionType = 'expense'
                entertainmentCounts[yearMonth] += 1
                assignedEntertainment += 1
            elif assignedTransport < 3 and date not in usedDates:
                category = 'Transport'
                transactionType = 'expense'
                transportCounts[yearMonth] += 1
                assignedTransport += 1
            elif assignedOther < 3 and date not in usedDates:
                category = 'Other'
                transactionType = 'expense'
                otherCounts[yearMonth] += 1
                assignedOther += 1
            else:
                break

            description = random.choice(descriptionDict[category])
            minAmount, maxAmount = amountRanges[category]
            amount = round(random.uniform(minAmount, maxAmount), 2)
            dataRows.append([date.strftime('%Y-%m-%d'), category, description, amount, transactionType])
            usedDates.add(date)

    for date in dates:
        if date in usedDates:
            continue

        yearMonth = date.strftime('%Y-%m')

        availableCategories = ['Shopping', 'Transport', 'Entertainment', 'Other', 'Freelance']

        if shoppingCounts[yearMonth] >= 6:
            availableCategories.remove('Shopping')
        if entertainmentCounts[yearMonth] >= 5:
            availableCategories.remove('Entertainment')
        if transportCounts[yearMonth] >= 9:
            availableCategories.remove('Transport')
        if freelanceCounts[yearMonth] >= 3:
            availableCategories.remove('Freelance')
        if otherCounts[yearMonth] >= 6:
            availableCategories.remove('Other')

        if 'Freelance' in availableCategories and random.random() > 0.5:
            category = 'Freelance'
            freelanceCounts[yearMonth] += 1
        elif shoppingCounts[yearMonth] < 4 and 'Shopping' in expenseCategoryPool:
            category = 'Shopping'
            shoppingCounts[yearMonth] += 1
        elif entertainmentCounts[yearMonth] < 2 and 'Entertainment' in expenseCategoryPool:
            category = 'Entertainment'
            entertainmentCounts[yearMonth] += 1
        elif transportCounts[yearMonth] < 8 and 'Transport' in expenseCategoryPool:
            category = 'Transport'
            transportCounts[yearMonth] += 1
        elif otherCounts[yearMonth] < 2 and 'Other' in expenseCategoryPool:
            category = 'Other'
            otherCounts[yearMonth] += 1
        else:
            category = random.choice(availableCategories)
            if category == 'Shopping':
                shoppingCounts[yearMonth] += 1
            elif category == 'Entertainment':
                entertainmentCounts[yearMonth] += 1
            elif category == 'Transport':
                transportCounts[yearMonth] += 1
            elif category == 'Other':
                otherCounts[yearMonth] += 1
            elif category == 'Freelance':
                freelanceCounts[yearMonth] += 1

        transactionType = 'expense' if category in expenseCategoryPool else 'income'
        description = random.choice(descriptionDict[category])
        minAmount, maxAmount = amountRanges[category]
        amount = round(random.uniform(minAmount, maxAmount), 2)
        dataRows.append([date.strftime('%Y-%m-%d'), category, description, amount, transactionType])
        usedDates.add(date)

    valid = True
    for yearMonth in datesByMonth.keys():
        if yearMonth not in salaryMonths:
            print(f"Validation failed: No Salary in {yearMonth}")
            valid = False
        if yearMonth not in investmentMonths:
            print(f"Validation failed: No Investment in {yearMonth}")
            valid = False
        if yearMonth not in healthMonths:
            print(f"Validation failed: No Health in {yearMonth}")
            valid = False
        bill_count = sum(1 for row in dataRows if row[1] == 'Bills' and row[0].startswith(yearMonth))
        if bill_count < len(descriptionDict['Bills']):
            print(f"Validation failed: Not enough Bills in {yearMonth}")
            valid = False
        if shoppingCounts[yearMonth] > 6:
            print(f"Validation failed: Too many Shopping transactions in {yearMonth}")
            valid = False
        if entertainmentCounts[yearMonth] > 5:
            print(f"Validation failed: Too many Entertainment transactions in {yearMonth}")
            valid = False
        if transportCounts[yearMonth] > 9:
            print(f"Validation failed: Too many Transport transactions in {yearMonth}")
            valid = False
        if freelanceCounts[yearMonth] > 3:
            print(f"Validation failed: Too many Freelance transactions in {yearMonth}")
            valid = False
        if otherCounts[yearMonth] > 6:
            print(f"Validation failed: Too many Other transactions in {yearMonth}")
            valid = False

    if valid:
        success = True
        print("All validations passed. CSV generation successful.")
    else:
        print(f"Attempt {attempt} failed validation. Trying again...")

if success:
    dataRows.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Category', 'Description', 'Amount', 'Type'])
        writer.writerows(dataRows)

    print("CSV file 'output.csv created successfully")
else:
    print(f"Ran all {max_attempts} attempts. Stopping.")