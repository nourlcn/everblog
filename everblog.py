from flask import Flask
from flask import render_template

#import sys
#import hashlib
#import binascii
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from time import time

glob={
    'lastupdate':time(),
    'tagGuids':[],  # [(id,name)]
    'noteGuids':[], # [(id,name)]
    'note_tag':{},
    'notebookGuids':[]
} # used as global var, quick response to user.


authToken = "fill your auth token"
evernoteHost = "sandbox.evernote.com"
userStoreUri = "https://" + evernoteHost + "/edam/user"

userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
userStore = UserStore.Client(userStoreProtocol)

noteStoreUrl = userStore.getNoteStoreUrl(authToken)
noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
noteStore = NoteStore.Client(noteStoreProtocol)

app = Flask(__name__)

def update_everblog_meta():
    glob['lastupdate'] = time()
    for tag in noteStore.listTags(authToken):
#        if tag.name == "blog":
        glob['tagGuids'].append((tag.guid,tag.name))

    nf = NoteStore.NoteFilter()
    nf.tagGuids = [id for id,name in glob['tagGuids'] if name == "blog"]

#    max_count = noteStore.findNoteCounts(authToken, nf, False)
#    max_count.tagCounts[nf.tagGuids[0]]
    for note in noteStore.findNotes(authToken, nf, 0, 50).notes:
        glob['noteGuids'].append((note.guid, note.title))
        glob['note_tag'][note.guid]=note.tagGuids

@app.route('/')
def note_list():
    now = time()
    if (now-glob['lastupdate']) > 1800:
        glob['lastupdate'] = now
        update_everblog_meta()

    return render_template('notelist.html', tag_list=glob['tagGuids'], \
        note_list=glob['noteGuids'], index=True)

@app.route('/<noteGuid>')
def get_note_by_guid(noteGuid):
    return str(noteStore.getNote(authToken, noteGuid, True, False, False, False).content)

@app.route('/tag/<tagGuid>')
def get_notes_by_tag(tagGuid):
    note_list= filter(lambda x: tagGuid in glob['note_tag'][x[0]], glob['noteGuids'])
#    print "note list is", note_list
    return render_template('notelist.html', tag_list=glob['tagGuids'], \
        note_list = note_list, index=False)

if __name__ == '__main__':
    update_everblog_meta()
#    print glob
#    get_notes_by_tag("5b93df05-7120-4470-aa87-22b704d5bbdf")
    app.run(debug=True)
