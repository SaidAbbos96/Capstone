import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from sqlalchemy import desc
from datetime import date

assistant_auth =   {
                    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlRLTZiTUpPVjBfTnd6ZmpQbklDViJ9.eyJpc3MiOiJodHRwczovL2t1YmVyeC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDIxODkxY2MxYWMwYzE0OGZmMzVkIiwiYXVkIjoiY2Fwc19pZCIsImlhdCI6MTU4ODg3MTI5NiwiZXhwIjoxNTg4OTU3Njk2LCJhenAiOiJoR1UzbGpnbHp0WDJUMkhCVDFWTTRQRFlYc0s0OXJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.TYR23ek2V9DaZeV7a37Ls45OV8KuLLu_5FSwTilduxWG8jtCG7NfmJjd93RSBpq2IZqJ-R1YMuwWZ0J9GpJE2itcGm6SWCoEPJpcwCWYmCUlsGNlIvMZHPGmRjs_IqlyEsdYqDi7ERLc0S-RXHvFt6JA6BnhNv62tBKpctH9XtYyF1xr9Pc-6F54Nnt7gZDtBo0KGCOZTWL85nkWhNnuodF5tW5o3pSnDLQD-3DS98PbDsT18UYLPTgEgKnJKcnELvARr88dSKqlLeRBExtKpWE-NIlsn33VK8FuXdlGIVm4FcCT7dkGIMB5nRUWtBrt_ZT9cP79GGmGfpw4M1yR6A"
                    }
director_auth_header =  {
                            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlRLTZiTUpPVjBfTnd6ZmpQbklDViJ9.eyJpc3MiOiJodHRwczovL2t1YmVyeC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDIyMjc2YjY5YmMwYzEyZmY3NTU2IiwiYXVkIjoiY2Fwc19pZCIsImlhdCI6MTU4ODg3MTQ0NiwiZXhwIjoxNTg4OTU3ODQ2LCJhenAiOiJoR1UzbGpnbHp0WDJUMkhCVDFWTTRQRFlYc0s0OXJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwibW9kaWZ5OmFjdG9yIiwibW9kaWZ5Om1vdmllIl19.J4OfdkGmUGxKmcoPqzZIt6UCn4VoLI50IGLWLyvELJU8BAPPL58p98f0IHkz_ExRO3aDnxinWAs646F1FwQXXzhDCDqMcLEmNCE2SJn94VU54kiL3XMESSFLbpL4D-V2nnXQXU0ZQgQcT3O4WRsiJ49LXrdKXtTptcmknOB88sSCr1wAw423DCKbPDX59pROA54Gf_9DoBxX8FwfHm1bqaVUk6HQcUt6-AGcix8NaFx_0q27MXymUOXc4Uq9bd_FY4pvfBvzWR6Koss23p-BwGpCykUh6l8g7R5HqCFGbL-_4xN6MVx_j0z6QoAYdgl2CUV7tc2xPia8P4lHuhwRJg"
                        }
producer_auth_header = {
                            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlRLTZiTUpPVjBfTnd6ZmpQbklDViJ9.eyJpc3MiOiJodHRwczovL2t1YmVyeC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDIyMjc2YjY5YmMwYzEyZmY3NTU2IiwiYXVkIjoiY2Fwc19pZCIsImlhdCI6MTU4ODg3MDk0NSwiZXhwIjoxNTg4OTU3MzQ1LCJhenAiOiJoR1UzbGpnbHp0WDJUMkhCVDFWTTRQRFlYc0s0OXJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwibW9kaWZ5OmFjdG9yIiwibW9kaWZ5Om1vdmllIl19.NDhIm3v6XzfmvFGDn2-8ej1U2HuAS0NIMfh_Jy4ECMk8IFW4zh1YJLkbjnbg5jvaTzyiQZP5h1Ghg0yxBxP3Wt_aF-vXXNa5mHsnXScNWDK_9_JsZDZBKbVq4Ur_iKOqyp35hCQfuw3UXr6m1jgtf8juXghGjGlom-8d9z3_x-SkRDcTQT7D9T9-2STLioAjhBo6DL9Kq-d1Oz5pAd5rm8Qdb_G3xLWdoe37ISzLRdmODSgmK2sYZjtn_vYWoL3hOd826g9wm9gkjr57MlPHPUUfPsC1f-g6UBEgPZQUD4E5fraiWX35vzDPyEFmyi2RVySmPYKZh1j57UdaYe5YoQ"
                        }

new_actor = {"name": "shokhrukhhan", "age": 41, "gender": "Male"}
new_movie = {"title": "topka", "release_date": date.today()}


class CastingTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        database_path = os.environ["DATABASE_URL"]
        setup_db(self.app, database_path)
        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # tests for POST /actors

    def test_add_actor(self):
        # add new actors: success scenario
        res = self.client().post(
            "/actors", json=new_actor, headers=director_auth_header
        )
        data = json.loads(res.data)
        Fout = open( "result_tests/test_add_actor.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])


    def test_add_actor_401(self):
        # add new actor: failure ,without authorization header
        res = self.client().post("/actors", json=new_actor)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_add_actor_401.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_actor_400(self):
        # add new actor: failure , without 'name' in json
        this_actor = {"age": 45}
        res = self.client().post(
            "/actors", json=this_actor, headers=director_auth_header
        )
        data = json.loads(res.data)
        Fout = open( "result_tests/test_add_actor_400.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'Please add "name" in the json')

    # tests for GET /actors
    def test_get_actors(self):
        # get actors at page=1
        res = self.client().get("/actors", headers=assistant_auth)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_get_actors.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_actors_404(self):
        # get actors at page=100
        res = self.client().get("/actors?page=100", headers=assistant_auth)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_get_actors_404.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "OOPS! No actors willing to work")

    def test_get_actors_401(self):
        # get actors: failure ,without authorization header
        res = self.client().get("/actors")
        data = json.loads(res.data)
        Fout = open( "result_tests/test_get_actors_401.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")


    def test_modify_actors_400(self):
        # update an actor , not sending json
        res = self.client().patch("/actors/1", headers=producer_auth_header)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_modify_actors_400.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "there is no json body")

    def test_modify_actors_403(self):
        # update an actor ,sending assistant header(doesn't contain required permissions)
        this_actor = {"name": "Priyanka Chopra"}
        res = self.client().patch("/actors/1", json=this_actor, headers=assistant_auth)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_modify_actors_403.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    # tests for DELETE /actors
    def test_delete_actor_404(self):
        # delete an actor , failure scenario: incorrect actor_id
        res = self.client().delete("/actors/10", headers=producer_auth_header)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_delete_actor_404.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "No actor with this id")

    def test_delete_actor_401(self):
        # delete an actor , without headers
        res = self.client().delete("/actors/1")
        data = json.loads(res.data)
        Fout = open( "result_tests/test_delete_actor_401.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_delete_actor(self):
        res = self.client().delete("/actors/1", headers=producer_auth_header)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_delete_actor.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 404)


    def test_add_movie_401(self):
        # add new movie: failure ,without authorization header
        res = self.client().post("/movies", json=new_movie)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_add_movie_401.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")


    # tests for GET /movies
    def test_get_movies(self):
        # get movies at page=1
        res = self.client().get("/movies?page=1", headers=assistant_auth)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_get_movies.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_movies_404(self):
        # get movies at page=100
        res = self.client().get("/movies?page=100", headers=assistant_auth)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_get_movies_404.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "OOPS! No one is making movies")


    # tests for PATCH /movies
    def test_modify_movies(self):
        # update an movie , sending id and json
        this_movie = {"title": "mahabharta"}
        res = self.client().patch(
            "/movies/1", json=this_movie, headers=producer_auth_header
        )
        data = json.loads(res.data)
        Fout = open( "result_tests/test_modify_movies.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"], 1)

    def test_modify_movies_400(self):
        # update an movie , not sending json
        res = self.client().patch("/movies/1", headers=producer_auth_header)
        data = json.loads(res.data)
        Fout = open( "result_tests/test_modify_movies_400.txt","w" ) 
        Fout.write(str(data))
        Fout.close()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "there is no json body")


if __name__ == "__main__":
    unittest.main()

