from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:\n\n".format(artist)
        result += "\n".join(album_names)
    return result


@route("/albums", method="POST")
def add_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    
    if album_data["year"] and not album_data["year"].isdigit():
        return "Указан некорректный год альбома. Ожидался формат YYYY (Например, 1999)"
    else:
        if album.save_album(album_data):
            return "Альбом {} успешно добавлен".format(album_data["album"])
        else:
            return HTTPError(409, "Альбом {} уже есть в базе данных.".format(album_data["album"]))
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)



# http -f POST localhost:8080/albums artist="Billie Eilish" genre="pop" year=2019 album="When we all fall asleep, where do we go?"
# http -f POST localhost:8080/albums artist="Sting" genre="pop" year=2013 album="The last ship"
