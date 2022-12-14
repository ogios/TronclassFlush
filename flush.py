from alive_progress import alive_bar
import requests.utils
import requests
import json
import re
import time
import click
from threading import Thread


class Flush:
    def __init__(self, courseURL: str, session: str, totalCount: int, isTeacher: bool = False, visitDuration: int = 60, threadCount: int = 5, progressBar: bool = True) -> None:
        self.flushURL = "http://lms.eurasia.edu/statistics/api/user-visits"
        self.courseURL = courseURL
        self.totalCount = totalCount
        self.threadCount = threadCount
        self.progressBar = progressBar
        self.n = int(self.totalCount/self.threadCount)
        self.cookie = requests.utils.cookiejar_from_dict({"session": session})
        self.data = {
            "org_id": 1,
            "is_teacher": isTeacher,
            "visit_duration": visitDuration,
            "user_id": "",
            "course_id": "",
        }
        self.count = 0
        self.threads: list[Thread] = []

    def getINFO(self) -> bool:
        res = requests.get(self.courseURL, cookies=self.cookie)
        if res.status_code == 200:
            user_id = re.findall(re.compile(
                'id=\"userId\".*?value=\"(.*?)\"', re.S), res.text)
            course_id = re.findall(re.compile(
                'id="courseId" value="(.*?)"', re.S), res.text)
            if (len(user_id) < 1 | len(course_id) < 1):
                self.printf("GetInfo Fatal")
                self.printf(f"user_id: {user_id}")
                self.printf(f"course_id: {course_id}")
                print(self)
                return False

            self.data["user_id"] = user_id[0]
            self.data["course_id"] = course_id[0]
            self.data = json.dumps(self.data)
            return True
        else:
            print(res)
            return False

    def _flush(self):
        n = 0
        for _ in range(self.n):
            res = requests.post(
                self.flushURL, cookies=self.cookie, data=self.data)
            if res.status_code != 204:
                self.printf(str(res.status_code))
            else:
                n += 1
            time.sleep(0.01)
            self.count += 1
        print(f"Thread done. POST success: {n}")

    def flush(self):
        if (not isinstance(self.data, str)):
            if self.getINFO():
                for _ in range(self.threadCount):
                    th = Thread(target=self._flush, daemon=True)
                    th.start()
                    self.threads += [th]
            else:
                raise Exception(
                    "[ GetInfo Fatal ] ?????????????????????????????????????????????????????????")

    def show(self):
        threads = self.threads
        if self.progressBar:
            with alive_bar(self.totalCount) as bar:
                last = 0
                while 1:
                    dead = True
                    for i in threads:
                        if i.is_alive():
                            dead = False
                            break
                    if dead:
                        bar(self.count-last)
                        break
                    count = self.count
                    if count != last:
                        bar(count-last)
                    last = count
                    time.sleep(0.1)
        else:
            while 1:
                dead = True
                for i in threads:
                    if i.is_alive():
                        dead = False
                        break
                if dead:
                    break
                time.sleep(1)

    def printf(string: str, end: str = "\n", sep: str = " ", flush: bool = False):
        ahead = time.strftime(" [ %Y-%m-%d %H:%M:%S ] - ", time.localtime())
        print(ahead+string, end=end, sep=sep, flush=flush)

    def __str__(self) -> str:
        string = ""
        string += f"flushURL: {self.flushURL}\n"
        string += f"courseURL: {self.courseURL}\n"
        string += f"totalCount: {self.totalCount}\n"
        string += f"threadCount: {self.threadCount}\n"
        string += f"n: {self.n}\n"
        string += f"cookies: {self.cookie}\n"
        string += f"data: {self.data}\n"
        return string


@click.command()
@click.option("-session", default="", help="login session")
@click.option("-url",  default="", help="course that need to be flushed")
@click.option("-count", type=int, default=100, help="Your purpose, Default 100")
def main(session, url, count) -> None:
    # if url == "":
    if (count == 100):
        print("?????? 100 ????????????????????????????????? -count ??????")
    else:
        print(f"?????? {count} ???")
    if len(re.findall(re.compile("^http://lms.eurasia.edu/course/\d*"), url)) == 1:
        if session != "":
            with open("conf.ini", "r+") as f:
                f.write(json.dumps({"session": session}))
        else:
            js: dict = {}
            with open("conf.ini", "r+") as f:
                conf = f.read()
                print("conf: ", conf)
                try:
                    js = json.loads(conf)
                except Exception as e:
                    print("No conf")
            if "session" in list(js.keys()):
                session = js["session"]
            else:
                print("No session")
                return
        # print('session:', session)
        # print("url:", url)
        f = Flush(courseURL=url, session=session,
                  totalCount=int(count), progressBar=True)
        f.flush()
        f.show()
        print(f.count)
    else:
        print("No courseURL input, use -url to set the course\nExample: http://lms.eurasia.edu/course/134766/my-stat")


if __name__ == "__main__":
    main()
