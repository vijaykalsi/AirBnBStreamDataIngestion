import json
import boto3
import calendar
from datetime import date, timedelta, datetime
import random

sqs_client = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/905418247818/AirbnbBookingQueue'  # replace with your SQS Queue URL

def rand_dates(max_days=5, year=None):
    
    while True:
        y = year or date.today().year
        m = random.randint(1, 3)
        d = random.randint(1, calendar.monthrange(y, m)[1])
        days = random.randint(1, max_days) if max_days > 0 else 0
        start_date = date(y, m, d)
        end_date = start_date + timedelta(days=days)
        return [str(start_date) , str(end_date)]
    

def generate_bookings():
    dt=rand_dates()
    booking_duration=(datetime.strptime(dt[1],'%Y-%m-%d').date() - datetime.strptime(dt[0], '%Y-%m-%d').date()).days
    location=["Delhi, India", "Mumbai, India", "New York, United States", "Dhaka, Bangladesh", "Kolkata, India", "Bangalore, India", "Chennai, India", "Los Angeles, United States", "Hyderabad, India", "Chicago, United States", "Pune, India", "Ahmedabad, India", "Chattogram, Bangladesh", "Surat, India", "Miami, United States", "Houston, United States", "Dallas, United States", "Philadelphia, United States", "Toronto, Canada", "Atlanta, United States", "Washington, United States", "Melbourne, Australia", "Sydney, Australia", "Boston, United States", "Kabul, Afghanistan", "Phoenix, United States", "Detroit, United States", "Montreal, Canada", "Seattle, United States", "Lucknow, India", "San Francisco, United States", "Jaipur, India", "San Diego, United States", "Minneapolis, United States", "Tampa, United States", "Brooklyn, United States", "Kanpur, India", "Denver, United States", "Gazipura, Bangladesh", "Vancouver, Canada", "Nagpur, India", "Queens, United States", "Brisbane, Australia", "Riverside, United States", "Las Vegas, United States", "Supaul, India", "Baltimore, United States", "Perth, Australia", "St. Louis, United States", "Portland, United States", "Vadodara, India", "San Antonio, United States", "Rajkot, India", "Indore, India", "Sacramento, United States", "Austin, United States", "Thane, India", "Orlando, United States", "Bhopal, India", "San Jose, United States", "Pittsburgh, United States", "Indianapolis, United States", "Pimpri-Chinchwad, India", "Manhattan, United States", "Cincinnati, United States", "Kansas City, United States", "Patna, India", "Cleveland, United States", "Bilaspur, India", "Ludhiana, India", "Agra, India", "Columbus, United States", "Madurai, India", "Jamshedpur, India", "Prayagraj, India", "Nasik, India", "Bronx, United States", "Virginia Beach, United States", "Charlotte, United States", "Faridabad, India", "Khulna, Bangladesh", "Calgary, Canada", "Meerut, India", "Adelaide, Australia", "Milwaukee, United States", "Providence, United States", "Jacksonville, United States", "Jabalpur, India", "Kalyan, India", "Vasai-Virar, India", "Najafgarh, India", "Varanasi, India", "Srinagar, India", "Nashville, United States", "Salt Lake City, United States", "Raleigh, United States", "Dhanbad, India", "Edmonton, Canada", "Amritsar, India"]
    index =random.randint(1, 98)
    return {
        "bookingid": random.randint(1000, 9999),
        "userId": random.randint(100, 999),
        "propertyId": random.randint(1, 100),
        "location": location[index],
        "start_date":dt[0],
        "end_date":dt[1],
        "price": round(random.uniform(10.0, 500.0), 2),
        "booking_duration":booking_duration
    }

def lambda_handler(event, context):
    i=0
    while(i<200):
        bookings = generate_bookings()
        print(bookings)
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(bookings)
        )
        i += 1
    
    return {
        'statusCode': 200,
        'body': json.dumps('Bookings data published to SQS!')
    }