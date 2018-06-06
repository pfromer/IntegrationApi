EJEMPLOS DE USO
}

---------------------------------
GET
http://localhost:5000/users
---------------------------------
POST
http://localhost:5000/room
{
        "id": "5",
        "name": "nueva sala",
		"token": "2222",
		"type": "group",
		"users": [		
			{
				"GWT_CHAT": [1,2,3]		
			},
			{
				"net core": [3,5,9]
			},			
			{
				"buatsaapp": [6,8]
			}
		
		]
}


-----------------------------------
POST
http://localhost:5000/message

{
        "idFrom": "5",
        "nameFrom": "juan",
		"idTo": "1",
		"platformTo": "GWT",
		"text", "hola",
		"token": "2222"
}

------------------------------------
POST
http://localhost:5000/user

{
        "id": "5",
        "name": "juan",
		"token": "2222"
}

-----------------
POST
http://localhost:5000/message

{
        "roomOriginalPlatform": "buatsapp",
        "roomId": 3,
        "senderId": 4,
		"senderPlatform": "GWT",
        "text": "hola",
		"token": "2222"
}