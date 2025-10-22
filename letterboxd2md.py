import csv
from datetime import datetime
import sys
import os
import re

def read_template(template_file):
    with open(template_file, 'r') as f:
        return f.read()

def parse_reviews(csv_file):
    reviews = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews.append(row)
    return reviews

def sanitize_filename(title):
    # Remove special characters and replace spaces with dashes
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')

def format_review(review):
    rating = review['Rating'] if review['Rating'] else '-'
    rewatch = ' 🔄' if review['Rewatch'] == 'Yes' else ''
    tags = f" #{review['Tags'].replace(', ', ' #')}" if review['Tags'] else ''
    
    review_text = review['Review'] if review['Review'] else '*Keine Bewertung*'
    date_obj = datetime.strptime(review['Date'], '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d.%m.%Y')
    
    return (f"# {review['Name']} ({review['Year']})\n\n"
           #f"Datum: {formatted_date}\n\n"
           f"⭐ {rating}{rewatch}\n\n" # {tags}\n\n"
           f"{review_text}\n\n"
           f"[Auf Letterboxd ansehen]({review['Letterboxd URI']})")

def create_review_file(review, template):
    # Create filename
    slug = f"{sanitize_filename(review['Name'])}-{review['Year']}"
    filename = slug + ".md"
    
    # Format the review content
    review_content = format_review(review)
        
    # Replace placeholder in template
    post_content = template.replace("REVIEWTEXT", review_content)

    # Update metadata in template
    post_content = post_content.replace("DATE-VORLAGE", review['Date'])
    post_content = post_content.replace("SLUG-VORLAGE", slug.lower())
    post_content = post_content.replace("TITLE-VORLAGE", f"Review: {review['Name']}")
    
    # Create output directory if it doesn't exist
    output_dir = "reviews"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write the file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    return filepath

def main():
    template = read_template('_VORLAGE.md')
    reviews = parse_reviews('reviews.csv')
    
    created_files = []
    for review in reviews:
        filepath = create_review_file(review, template)
        created_files.append(filepath)
    
    print(f"Created {len(created_files)} review files:")
    for filepath in created_files:
        print(f"- {filepath}")

if __name__ == '__main__':
    main()