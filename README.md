# MovieReviews by bkh727 and gvt504

## How to run

- Initialize postgres database and remember your credentials!
- Go to the directory MovieReviews if you are not already in it
- Make sure you have all the required libraries by running `pip install -r requirements.txt`
- Create a .env file with the following template: `DB_NAME=your_db_name`
  `DB_HOST=your_db_host`
  `DB_USER=your_db_user`
  `DB_PASSWORD=your_db_password`
- Seed your database by running `python MovieReviewsApp/setup_db.py` make sure that you are in the directory MovieReviews and not in MovieReviewsApp!
- You can reset the database by running `python MovieReviewsApp/reset_db.py`
- You can now run the app by running `python run.py`
