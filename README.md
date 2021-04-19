# Steps to run the project

1. Clone this repo on to your local computer.

2. Create a virtual environment using **pipenv** inside the project root directory by running

    ```pipenv --three``` in the command line inside the project directory

3. If you don't have pipenv installed, install it using the pip command

   ​	``` pip install --user pipenv``` from cmd.

4. Start pipenv shell inside your project root using ```pipenv shell``

5. Install the required dependencies from requirements.txt using 

   ​	```pipenv install <package_name>==<package_version>```

   or all dependencies using ```pip install -r requirements.txt```

7. Create a .env file inside the project root directory and add your POSTGRES credentials in it.

   Here's how:

   ```.env
   POSTGRES_USERNAME = your_postgres_user_id
   POSTGRES_PASSWORD = your_postgres_password
   POSTGRES_IP = 127.0.0.1
   POSTGRES_PORT = postgres_port(default= 5432)
   ```

8. then run

   ```py
   python manage.py migrate
   ```

9. create admin account

```py
python manage.py createsuperuser
```

10. then

```py
python manage.py makemigrations
```

11. to make migrations for the app

12. then again run

```py
python manage.py migrate
```

13. to start the development server

```py
python manage.py runserver
```

14. and open localhost:8000 on your browser to view the app.

# API Endpoints

###### BASE_URL= 127.0.0.1:8000/api

1. **All Pizzas**

   * Method - ```GET```

   * Url -  BASE_URL/pizza

   * Query Params: (Optional - to filter pizzas)

     * size=[Small, Medium, Large]
     * type= [regular, square]

   * Example:

     * Url: 127.0.0.1:8000/api/pizza?size=large

     * Response:

       ```json
       [
           {
               "id": 7,
               "pizza_type": "square",
               "pizza_size": "Large",
               "pizza_topping": [
                   "Cheese",
                   "Olives",
                   "Corn"
               ]
           },
           {
               "id": 8,
               "pizza_type": "regular",
               "pizza_size": "Large",
               "pizza_topping": [
                   "Cheese",
                   "Onion",
                   "Capsicum",
                   "Olives"
               ]
           }
       ]
       ```

 2. **Create Regular Pizza**

    * Method: ```POST```

    * Url: BASE_URL/pizza/createRegular

    * Body: 

      ```json
      "size":"small",
      "topping": [
          "Cheese",
          "capsicum",
          "Onion",
          "olives"
      ]
      ```

      **Size** and **topping** both are required otherwise **412 error** is returned

      ```{"error": "Size is required"}```

      ```{"error": "One Topping is required"}```

      

      For **invalid** size or topping **404 error** is returned

      ```{"error": "Invalid Size"}```

      ```{"error": "Invalid Topping"}```

    * Success Code - ```201 Created```

    * Success Response: (Newly created pizza)

      ```json
      {
          "id": 9,
          "pizza_type": "regular",
          "pizza_size": "Small",
          "pizza_topping": [
              "Cheese",
              "Onion",
              "Capsicum",
              "Olives"
          ]
      }
      ```

    3. **Create Square Pizza**

       * Url: BASE_URL/createSquare
       * Everything else same as above

    4. **View Individual Pizza**

       * Url: BASE_URL/pizza/<pizza_id>

       * Method: ```GET```

       * Success Code (Pizza Exists): ```200 OK```

       * Success Response: 

         ```json
         {
             "id": 9,
             "pizza_type": "regular",
             "pizza_size": "Small",
             "pizza_topping": [
                 "Cheese",
                 "Onion",
                 "Capsicum",
                 "Olives"
             ]
         }
         ```

         

       * Failure Code(Pizza Does Not Exist): ```404 Not Found```

       * Failure Response:

         ```json
         {
             "error": "Pizza Not Found"
         }
         ```

    5. **Delete Pizza**

       * Url: BASE_URL/pizza/<pizza_id>

       * Method: ```DELETE```

       * Success Code (Pizza Deleted): ```200 OK```

       * Success Response: 

         ```json
         {
             "success": "Pizza Deleted"
         }
         ```

       * Failure Code (Pizza Does Not Exist): ```404 Not Found```

       * Failure Response: 

         ```json
         {
             "error": "Pizza Not Found"
         }
         ```

    6. **Update Pizza**

       * Url: BASE_URL/pizza/<pizza_id>

       * Method: ```PUT```

       * Body: 

         ```json
         "size":"small",
         "type": "square",
         "topping": [
             "Cheese",
             "capsicum",
             "Onion",
             "olives"
         ]
         ```

         All fields are **optional**, but incorrect values will return an error ``404 Not Found```

       * Success Code (No errors in the body and pizza exists):  ```202 Accepted```

       * Success Response: Same as *View Individual Pizza* but with updated valued

       * Failure Code (Pizza Does Not Exist): ```404 Not Found```

       * Failure Response: 

         ```json
         {
             "error": "Pizza Not Found"
         }
         ```

         

# Admin Panel

###### ADMIN_URL= BASE_URL/admin



- Log in to the admin panel to view all orders, toppings, sizes and their details.
- Filters have been added to the apps
- Admin can create a new size, topping or pizza.