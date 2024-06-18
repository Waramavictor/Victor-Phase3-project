
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Appointment, Vote

def create_appointment(session, name, date_time):
    appointment = Appointment(name=name, date_time=date_time)
    session.add(appointment)
    session.commit()

def get_appointments(session):
    appointments = session.query(Appointment).all()
    return appointments

def create_vote(session, appointment_id, vote):
    vote = Vote(appointment_id=appointment_id, vote=vote)
    session.add(vote)
    session.commit()

def get_votes(session, appointment_id):
    votes = session.query(Vote).filter_by(appointment_id=appointment_id).all()
    return votes

def cancel_appointment(session, appointment_id):
    appointment = session.query(Appointment).get(appointment_id)
    if appointment:
        appointment.cancelled = True
        session.commit()
        print("Appointment cancelled successfully!")
    else:
        print("Appointment not found.")

def main():
    engine = create_engine('sqlite:///appointments.db')
    Appointment.metadata.create_all(engine)
    Vote.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1. Book an appointment")
        print("2. View previous appointments")
        print("3. Vote on an appointment")
        print("4. Cancel an appointment")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            date_str = input("Enter date and time (YYYY-MM-DD HH:MM), or just date (YYYY-MM-DD): ")
            try:
                date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            except ValueError:
                # If only the date is provided, set the time part to 00:00
                date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').replace(hour=0, minute=0)
            create_appointment(session, name, date_time)
            print("Appointment booked successfully!")
        elif choice == '2':
            appointments = get_appointments(session)
            if appointments:
                print("Previous appointments:")
                for appointment in appointments:
                    print(f"ID: {appointment.id}, Name: {appointment.name}, Date: {appointment.date_time}, Cancelled: {appointment.cancelled}")
            else:
                print("No previous appointments.")
        elif choice == '3':
            appointment_id = int(input("Enter the appointment ID to vote on: "))
            vote = int(input("Enter your vote (1 for yes, 0 for no): "))
            create_vote(session, appointment_id, vote)
            print("Vote cast successfully!")
        elif choice == '4':
            appointment_id = int(input("Enter the appointment ID to cancel: "))
            cancel_appointment(session, appointment_id)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()

if __name__ == "__main__":
    main()