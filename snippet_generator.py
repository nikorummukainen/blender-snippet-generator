import bpy
import json
import collections
from collections import OrderedDict
from os import path

bl_info = {
    "name": "snippet generator",
    "description": "Adds funtionality to blender text editor to convert/export code to snippets",
    "author": "Niko Rummukainen",
    "version": (0, 9, 0),
    "blender": (2, 9, 0),
    "location": "Text Editor",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Code" }

def readfile(filepath):
    '''
    reads file in filepath, returns files lines as list
    :filepath:filepath: filepath to file
    '''
    with open(filepath, 'r') as file:
        return file.readlines()

def file_to_json_snippet(jsonfile, file):
    '''
    For easier creation of code snippets Function loads .py file reads it and writes it to as is into json file. 
    :jsonfile:filepath: filepath to .json file, file will be turncated if exists, will be created if doesn't exist.
    :file:filepath: filepath to .py file thath is turned in to json snippet.
    '''
    with open(jsonfile, 'w') as json_file:
        json_obj = OrderedDict()
        key = ''.join(bpy.path.basename(file).split('.')[:-1]).replace(' ', '_')
        json_obj[key] = OrderedDict()
        json_obj[key]['prefix'] = key.replace('_', ' ')
        json_obj[key]['body'] = readfile(file)
        json_obj[key]['description'] = str('short description')
        json.dump(json_obj, json_file, sort_keys=False, indent=4)

    return jsonfile

def edit_text_to_list(context):
    text = context.edit_text
    return list(line.body for line in text.lines)

def edit_text_to_json_snippet(context, jsonfile):
    '''
    For easier creation of code snippets Function loads .py file reads it and writes it to as is into json file. 
    :context:context: blender file editor context
    :jsonfile:filepath: filepath to .json file, file will be turncated if exists, will be created if doesn't exist.
    '''
    with open(jsonfile, 'w') as json_file:
        json_obj = OrderedDict()
        key = ''.join(str(bpy.path.basename(jsonfile)).split('.')[:-1]).replace('_', ' ')
        json_obj[key] = OrderedDict()
        json_obj[key]['prefix'] = key.replace('_', ' ')
        json_obj[key]['body'] = edit_text_to_list(context)
        json_obj[key]['description'] = str('short description')
        json.dump(json_obj, json_file, sort_keys=False, indent=4)

    return jsonfile

class ConvertFiles(bpy.types.Operator):
    bl_idname = "text_exitor.convert_files"
    bl_label = "files to snippets"
    bl_description = "Converts files to json snippets"
    bl_options = {"REGISTER"}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')
    filename = bpy.props.StringProperty(subtype='FILE_NAME')
    directory = bpy.props.StringProperty(subtype='DIR_PATH')
    files = bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        extensions = ['.py', '.osl']
        '''
        for future support could extend glsl shaders? with .vert - a vertex shader
        .tesc - a tessellation control shader
        .tese - a tessellation evaluation shader
        .geom - a geometry shader
        .frag - a fragment shader
        .comp - a compute shader
        '''
        files = [self.directory+file.name for file in self.files if '.'+''.join(file.name.split('.')[-1:]) in extensions]
        for file in files:
            json_file = ''.join(str(file).split('.')[:-1])+'.json'
            file_to_json_snippet(json_file, file)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ConvertTexteditor(bpy.types.Operator):
    bl_idname = "text_editor.convert_text_editor"
    bl_label = "text to snippet"
    bl_description = "Convert code in texteditor to json snippet"
    bl_options = {"REGISTER"}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')
    filename = bpy.props.StringProperty(subtype='FILE_NAME')
    directory = bpy.props.StringProperty(subtype='DIR_PATH')
    files = bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #save current open text editor file
        json_file = ''.join(str(self.filepath).split('.')[:-1])+'.json'
        edit_text_to_json_snippet(context, json_file)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# class SnippetGeneratorPanel(bpy.types.Panel):
#     bl_idname = "text_editor.snippet_generator"
#     bl_label = "Snippet"
#     bl_space_type = "TEXT_EDITOR"
#     bl_region_type = "UI"
#     bl_category = "snippets"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator(ConvertFiles.bl_idname)
#         row = layout.row()
#         row.operator(ConvertTexteditor.bl_idname)        

def menu_func_convert_files(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(ConvertFiles.bl_idname)

def menu_func_convert_texteditor(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(ConvertTexteditor.bl_idname)

def register():
    bpy.utils.register_module(__name__)
    bpy.types.TEXT_MT_text.append(menu_func_convert_files)
    bpy.types.TEXT_MT_text.append(menu_func_convert_texteditor)
    print('Registered Addon: Snippet Generator')

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.TEXT_MT_text.remove(menu_func_convert_files)
    bpy.types.TEXT_MT_text.append(menu_func_convert_texteditor)

if __name__ == "__main__":
    register()    