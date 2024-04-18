from seek_helper import SeekHelper

token = 'ZXzWwOOqn2tk8fwLVOoV7515i6JyPI-ywidEZwzM'

seek_helper = SeekHelper(token, 'http://localhost:3000',
                         '/home/dbueno/projects/seek_helper/output')

# investigation = seek_helper.Investigation
# study = seek_helper.Study
# assay = seek_helper.Assay

# data_file = seek_helper.DataFile
# print(data_file.get(1))
# print(data_file.get(5))

# print(investigation.get())
# print(study.get())
# print(assay.get())

# print(data_file.get())
# print(data_file.download(10))

project = seek_helper.Project
p = project.get(1)
print(p)
# project.download_data_files(1)

# payload_create = {
#     "data": {
#         "type": "investigations",
#         "attributes": {
#             "title": "Investigation API Test",
#             "description": "blablabla",
#             "other_creators": "Bueno, Danilo"
#         },
#         "relationships": {
#             "projects": {
#                 "data": [
#                     {
#                         "type": "projects",
#                         "id": "1"
#                     },
#                 ]
#             },
#         }
#     }
# }

# payload_update = {
#     "data": {
#         "type": "investigations",
#         "id": "2",
#         "attributes": {
#             "description": "new description 2",
#         },
#     }
# }
