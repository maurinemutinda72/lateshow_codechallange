import csv
import os
from models import db, Episode, Guest, Appearance
from app import app

def clear_data():
    """Clear existing data in the database to prevent duplicates."""
    with app.app_context():
        try:
            
            db.session.query(Appearance).delete()
            db.session.query(Guest).delete()
            db.session.query(Episode).delete()
            db.session.commit()
            print("Existing data cleared successfully")
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing data: {str(e)}")

def load_data():
    """Load data from CSV and insert into the database."""
    seed_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed.csv')
    if not os.path.exists(seed_file_path):
        print(f"Error: seed file not found at {seed_file_path}")
        return
    
    with app.app_context():
        try:
            with open(seed_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  
                
                episode_number = 1  
                
                for row in csv_reader:
                    if len(row) < 5:  
                        continue
                        
                    year, occupation, date, show_group, guest_name = row
                    
                    
                    guest = Guest.query.filter_by(name=guest_name).first()
                    if not guest:
                        guest = Guest(name=guest_name, occupation=occupation)
                        db.session.add(guest)
                        db.session.commit()

                    
                    episode = Episode.query.filter_by(date=date).first()
                    if not episode:
                        episode = Episode(date=date, number=episode_number)
                        db.session.add(episode)
                        db.session.commit()
                        episode_number += 1
                    
                    
                    appearance = Appearance(
                        rating=3,
                        episode_id=episode.id,
                        guest_id=guest.id
                    )
                    db.session.add(appearance)
                
                db.session.commit()
                print("Data has been successfully loaded.")
        except Exception as e:
            db.session.rollback()
            print(f"Error loading data: {str(e)}")

def main():
    """Create tables, clear existing data and load new data."""
    with app.app_context():
        # Creating all tables
        db.create_all()
        print("Database tables created")
    
   
    clear_data()
    load_data()

if __name__ == "__main__":
    main()