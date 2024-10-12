from rest_framework.test import APITestCase,APIClient
from users.models import User
from .models import Tweet

class TestTweets(APITestCase):
    PAYLOAD="테스트입니다."
    PUT_PAYLOAD = "수정 테스트입니다."

    def setUp(self):
        self.client = APIClient() # 유저 인증을 위해
        self.USER = User.objects.create_user(
            username="1234",
            password="q1w2e3r4",
            user_nickname="dog",
        )

        Tweet.objects.create(
            payload="테스트입니다?",
            user=self.USER,
        )
        Tweet.objects.create(
            payload=self.PAYLOAD,
            user=self.USER,
        )

    def test_get_tweets(self):
        response = self.client.get("/api/v1/tweets/")
        print(response)
        data = response.json()
        
        self.assertEqual(
            response.status_code,
            200,
            "응답 코드가 200이 아닙니다.",
        )
        self.assertIsInstance(
            data,
            list,
            "데이터가 의도된(리스트)형태로 오지 않았습니다."
        )
        self.assertEqual(
            len(data),
            2,
            "반환된 데이터의 수가 의도된 수치가 아닙니다."
        )
        self.assertEqual(
            data[-1]["payload"],
            self.PAYLOAD,
            "마지막 데이터가 비교 대상과 값이 다릅니다."
        )

    # 데이터 추가 테스트
    def test_post_tweets(self):
        self.client.force_authenticate(user=self.USER)  # 사용자 인증 / GPT한테 물어보니, 해당 방법을 알려줬습니다.
        response = self.client.post(
            "/api/v1/tweets/",
            data={
                "payload": self.PAYLOAD,
            },
        )
        data = response.json()
        print(data)
        self.assertEqual(
            response.status_code,
            200,
            "응답 코드가 200이 아닙니다.",
        )
        self.assertEqual(
            data["user"]["username"],
            self.USER.username,
            "입력된 데이터의 유저가 의도된 값과 다릅니다."
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
            "입력된 데이터가 의도된 값과 다릅니다."
        )

        response = self.client.get("/api/v1/tweets/")
        print(response)
        data = response.json()
        self.assertEqual(
            len(data),
            3,
            "반환된 데이터의 수가 의도된 수치가 아닙니다."
        )

        response = self.client.post(
            "/api/v1/tweets/",
        )
        print(response)
        data = response.json()
        self.assertEqual(
            response.status_code,
            400,
            "응답 코드가 400이 아닙니다.",
        )

    # 데이터 받기 테스트
    def test_get_tweet(self):
        response = self.client.get("/api/v1/tweets/2/")
        print(response)
        data = response.json()
        
        self.assertEqual(
            response.status_code,
            200,
            "응답 코드가 200이 아닙니다.",
        )
        self.assertIsInstance(
            data,
            dict,
            "의도된 형태로 데이터가 반환되지 않았습니다."
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
            "데이터의 내용이 의도된 값과 다릅니다."
        )

    # 데이터 수정 테스트
    def test_put_tweet(self):
        self.client.force_authenticate(user=self.USER)  # 사용자 인증
        response1 = self.client.put(
            "/api/v1/tweets/2/",
            data={
                "payload": self.PUT_PAYLOAD,
            },
        )
        data = response1.json()
        print(data)
        self.assertEqual(
            data["user"]["username"],  # 직렬화된 user의 username 비교
            self.USER.username,
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )
        self.assertEqual(
            data[-1]["payload"],
            self.PAYLOAD,
            "데이터가 정상적으로 입력되지 않은거같습니다."
        )

    def test_delete_tweet(self):
        self.client.force_authenticate(user=self.USER)  # 사용자 인증
        response = self.client.delete("/api/v1/tweets/2/")
        data = response.json()
        print(data)
