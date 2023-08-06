import os
# import sys
import base64
import json
import requests
from tempfile import TemporaryDirectory
from typing import TypedDict, Literal, Any, Union
from requests import Session, Response
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis

OpenCloudAssetTypeName = Literal["Audio", "Decal", "Model"]
# OpenCloudAssetTypeValue = Literal[1,2,3]
HttpMethod = Literal["POST", "GET", "PATCH", "DELETE"]

LEGACY_AUDIO_URL = "https://publish.roblox.com/v1/audio"
LEGACY_IMAGE_URL = "https://data.roblox.com/data/upload/json?assetTypeId=13"
LEGACY_MODEL_URL = "https://data.roblox.com/data/upload/json?assetTypeId=10"
LEGACY_PACKAGE_URL = "https://data.roblox.com/data/upload/json?assetTypeId=28"
LEGACY_ANIMATION_URL = "https://data.roblox.com/data/upload/json?assetTypeId=20"
LEGACY_MESH_URL = "https://data.roblox.com/data/upload/json?assetTypeId=35"
LEGACY_MESH_URL = "https://data.roblox.com/data/upload/json?assetTypeId=35"
ASSET_URL = "https://apis.roblox.com/assets/v1/assets"

# ASSET_TYPE: dict[OpenCloudAssetTypeName, OpenCloudAssetTypeValue] = {
# 	"Audio": 1,
# 	"Decal": 2,
# 	"Model": 3,
# }

LIMITS = {
	"Audio": {
		"duration": 60*7,
		"uploads_per_month": 100,
		"is_updatable": False,
	},
	"Decal": {
		"is_updatable": False
	},
	"Model": {
		"is_updatable": True
	},
}

OPEN_CONTENT_CLOUD_TYPE = {
	"Audio": {
		".mp3": "audio/mpeg",
		".ogg": "audio/ogg"
	},
	"Decal": {
		".png": "image/png",
		".jpeg": "image/jpeg",
		".bmp": "image/bmp",
		".tga": "image/tga",
	},	
	"Model": {
		".fbx": "model/fbx",
	},	
}

StatusCode = Literal[
	200, # success
	400, # no file
	401, # auth denied
	403, #token validation fail / permission fail
	404, # target item does not exist
	429, # rate limited
]

class OpenCloudCreator(TypedDict):
	userId: int | None
	groupId: int | None

class OpenCloudCreationContext(TypedDict):
	creator: OpenCloudCreator
	expectedPrice: int

class OpenCloudAssetInfo(TypedDict):
	path: str | None
	revisionId: str | None
	revisionCreateTime: str | None

class OpenCloudCreationAsset(OpenCloudAssetInfo):
	description: str
	displayName: str
	assetType: OpenCloudAssetTypeName
	creationContext: OpenCloudCreationContext

class OpenCloudUpdateAsset(OpenCloudAssetInfo):
	assetId: int
	description: str | None
	displayName: str | None

OpenCloudAsset = Union[OpenCloudUpdateAsset, OpenCloudCreationAsset]

class OpenCloudStatus(TypedDict):
	code: StatusCode
	message: str
	details: list[str]

class OpenCloudOperation(TypedDict):
	path: str
	metadata: str
	done: bool
	error: str
	response: OpenCloudStatus

def _get_name_from_path(path: str) -> str:
	return os.path.splitext(str(os.path.basename(path)))[0]

class Publisher():
	group_id: int | None
	user_id: int | None
	place_key: str | None
	asset_key: str | None
	universe_registry: dict[int, int]
	session: Session

	def __init__(self, 
		cookie: str | None = None, 
		place_key: str | None = None, 
		asset_key: str | None = None,
		group_id: int | None = None,
		user_id: int | None = None
	):
		self.universe_registry = {}
		self.group_id = group_id
		self.user_id = user_id
		self.place_key = place_key
		self.asset_key = asset_key
		self.session = Session()
		self.session.cookies[".ROBLOSECURITY"] = cookie
		self.session.headers["User-Agent"] = "Roblox/WinInet"
		self.session.headers["Requester"] = "Client"
		self.session.headers['access-control-expose-headers'] = "x-csrf-token"

	def get_universe_id_from_place_id(self, place_id: int) -> int:
		if place_id in self.universe_registry:
			return self.universe_registry[place_id]

		universe_id: None | int = None
		for place in json.loads(self.session.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}").text):
			universe_id = int(place["universeId"])

		assert universe_id, f"bad universe_id for place_id {place_id}"

		self.universe_registry[place_id] = universe_id

		return universe_id

	def get_asset_id_from_operations_id(self, operations_id: str) -> int | None:
		# print(content_data)
		response = self.session.request(
			method="GET",
			url = f'https://apis.roblox.com/assets/v1/operations/{operations_id}',
			headers={
				"x-api-key": self.asset_key,
			}
		)
		content_data = json.loads(response.text)

		if "response" in content_data:
			response_data = content_data["response"]
			if "assetId" in response_data:
				return int(response_data["assetId"])
			else:
				return None
		else:
			return None

	def _creation_request(self, file_path: str, name: str, description: str, publish_to_group=True) -> str:

		with open(file_path, "rb") as file:
			binary_data = file.read()

		file_base, file_ext = os.path.splitext(file_path)

		file_type: None | str = None
		asset_type: None | str = None
		for type_category, type_registry in OPEN_CONTENT_CLOUD_TYPE.items():
			if file_ext in type_registry:
				asset_type = type_category
				file_type = type_registry[file_ext]

		assert file_type and asset_type, f"bad file type for {file_path}"

		request_payload : OpenCloudCreationAsset = {
			"assetType": asset_type,
			"displayName": name,
			"description": description,
			"creationContext": {},
		}

		if publish_to_group:
			request_payload ["creationContext"]["creator"] = {
				"groupId": self.group_id,
			}
		else:
			request_payload ["creationContext"]["creator"] = {
				"userId": self.user_id,
			}
		
		data = {
			'request': json.dumps(request_payload)
		}

		headers={
			"x-api-key": self.asset_key,
		}

		response: Response = self.session.request(
			method="POST",
			url=ASSET_URL,
			headers=headers,
			files={
				'fileContent': (file_path, binary_data, file_type)
			},
			data=data,
		)

		# print(response)
		# print(response.text)
		content_data = json.loads(response.text)
		if "path" in content_data:
			return content_data["path"].replace("operations/", "")
		else
			raise ValueError(f"bad response {content_data}")
	def _token_authorized_request(self, method: HttpMethod, url: str, **kwargs) -> Response | None:

		response = self.session.request(method, url, **kwargs)

		method = method.lower()
		if method in ["post", "put", "patch", "delete"]:
			if "x-csrf-token" in response.headers:
				self.session.headers["x-csrf-token"] = response.headers["x-csrf-token"]
				if response.status_code == 403:
					return self.session.request(method, url, **kwargs)
		return None

	def update_place(self, file_path: str, place_id: str):
		# print(f"posting place {file_path} to {place_id}")
		universe_id = self.get_universe_id_from_place_id(place_id)

		post_url = f"https://apis.roblox.com/universes/v1/{universe_id}/places/{place_id}/versions?versionType=Published"
		x = requests.post(
			post_url, 
			data=open(file_path, mode='rb'),
			headers={
				"Content-Type": "application/octet-stream",
				"x-api-key": self.place_key,
			}
		)
		# print(x.text)


	def post_image(self, file_path: str, name: str | None = None, publish_to_group=True, description: str | None = None) -> int | None:
		if not name:
			name = _get_name_from_path(file_path)

		assert name, f"bad name for {file_path}"	

		if not description:
			description = f"{name} decal"

		return self._creation_request(file_path, name, description, publish_to_group)			

	def post_audio(self, file_path: str, name: str | None = None, publish_to_group=True, description: str | None = None) -> int | None:
		if not name:
			name = _get_name_from_path(file_path)

		assert name, f"bad name for {file_path}"	

		if not description:
			description = f"{name} sound"


		return self._creation_request(file_path, name, description, publish_to_group)			

	def post_mesh_as_model(self, file_path: str, name: str | None = None, publish_to_group=True, description: str | None = None) -> int | None:
		if not name:
			name = _get_name_from_path(file_path)

		assert name, f"bad name for {file_path}"	

		if not description:
			description = f"{name} mesh model"

		return self._creation_request(file_path, name, description, publish_to_group)				

	# might be broken
	def legacy_publish_decal(self, file_path: str, name: str | None = None, publish_to_group=True) -> int | None:	
		# print("posting decal: "+file_path)

		if not name:
			name = _get_name_from_path(file_path)

		assert name, f"bad name for {file_path}"	

		param_data = {
			'name': name,
			'description': name
		}
		if publish_to_group:
			param_data["groupId"] = self.group_id
		else:
			param_data["userId"] = self.user_id

		response = self._token_authorized_request(
			"POST", LEGACY_IMAGE_URL, 
			data = open(file_path, mode='rb').read(), 
			params = param_data
		)

		data = json.loads(response.content.decode("utf-8"))

		if "BackingAssetId" in data:
			assetId = data["BackingAssetId"]
			return assetId
		else:
			print("Failed")
			print(response.content)
			return -1


	def legacy_publish_audio(self, file_path: str, name: str | None = None, publish_to_group=True) -> int | None:	
		# print("posting audio: "+file_path)

		if not name:
			name = os.path.splitext(str(os.path.basename(file_path)))[0]

		assert name, f"bad name for {file_path}"

		file = open(file_path, mode='rb')
		binary_data = base64.b64encode(file.read())
		binary_str = binary_data.decode("utf-8")

		duration: int | None
		file_size = os.path.getsize(file_path)
		base, ext = os.path.splitext(file_path)

		if ext == ".mp3":
			mp3_audio = MP3(file_path)
			mp3_audio_info = mp3_audio.info
			duration = int(mp3_audio_info.length)
			
		elif ext == ".ogg":
			ogg_audio = OggVorbis(file_path)
			ogg_audio_info = ogg_audio.info
			duration = int(ogg_audio_info.length)

		assert duration, f"bad file {file_path}"
		
		json_data = {
			"name": name,
			"file": binary_str,
			"paymentSource": "string",
			"estimatedFileSize": file_size,
			"estimatedDuration": duration,
			"assetPrivacy": "Private"
		}
		if publish_to_group:
			json_data["groupId"] = self.group_id
		else:
			json_data["userId"] = self.user_id

		response = self._token_authorized_request(
			"POST", LEGACY_AUDIO_URL, 
			json = json_data, 
			headers={
				"Content-Type": "application/json",
			}
		)
		data = json.loads(response.content.decode("utf-8"))
		if "Id" in data:
			assetId = data["Id"]
			return assetId
		else:
			print("Failed")
			print(response.content)
			return -1

# publisher = Publisher(
# 	cookie = sys.argv[2].replace("LINE", "|"), 
# 	place_key = sys.argv[1], 
# 	asset_key = sys.argv[1], 
# 	group_id = int(sys.argv[3]), 
# 	user_id = int(sys.argv[4]), 
# )		

# result_id = publisher.legacy_publish_audio("audio_test.mp3", publish_to_group=False)
# result_id = publisher.legacy_publish_decal("logo_test.png", publish_to_group=False)
# print("operation_id", result_id)

