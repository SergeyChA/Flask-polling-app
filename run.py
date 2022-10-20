from pollingsite import create_app, db


app = create_app()

# Create Tables
with app.app_context():
    db.create_all()


if __name__ == '__name__':
    app.run(debug=True)
