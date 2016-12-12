# cbDocNameChanger
A python script that takes in a json file to rename documents keys in multiple buckets.  It handles documents, and ziped files.

Executed on the localhost of the couchbase machine, this takes in a json file that is a dictionary with key values of buckets.  The value of these keys is another dictionary with key value pair of current document name, and desired document name.

IE:
{
  "bucket1":
  {
    "docName1":"docName2",
    "docXXX":"docYYY"
  },
  "bucket3":
  {
    "doc123":"doc321"
  }
}

this will make document docName1 be renamed to docName2 in bucket1.  Along with changin docXXX -> docYY in bucket1, and doc123->doc321 in bucket3.
