from flask import Flask, request, jsonify
from model import Base, Alumnos, get_engine, get_session
import os

app=Flask(__name__)

def create_tables():
    """Create all tables in the database"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tables created successfully")

def insert_data():
    """Insert sample data into the database"""
    session = get_session()
    alumnos = [
        Alumnos(name="Pablo", email="palandeta@utn.edu.ec"),
        Alumnos(name="Andres", email="landeta_p@yahoo.com")
        ]
    session.add_all(alumnos)
    session.commit()
    print(f"Inserted {len(alumnos)} students")

if __name__ == "__main__":
    create_tables()
    insert_data()
    port = int(os.getenv("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
