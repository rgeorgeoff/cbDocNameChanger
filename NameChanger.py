from couchbase.transcoder import Transcoder
from couchbase import FMT_BYTES
from pprint import pprint
import sys
import json
import base64
import zlib

class ZlibTranscoder(Transcoder):
    def decode_value(self, value, flags):
        if flags & 2:
            value = zlib.decompress(value, 16 + zlib.MAX_WBITS)
            flags &= ~2
        return super(ZlibTranscoder, self).decode_value(value, flags)

    def encode_value(self, value, fmt):
        encoded, flags = super(ZlibTranscoder, self).encode_value(value, fmt)
        if len(encoded) >= 16384:
            compressor = zlib.compressobj(6, zlib.DEFLATED, 16 + zlib.MAX_WBITS)
            encoded = compressor.compress(encoded)
            encoded += compressor.flush()
            flags |= 2
        return (encoded, flags)

with open('dataToChange.json') as data_file:    
    data = json.load(data_file)
pprint(data)

RAW_TYPECODE = 0x0A000000
DATABASE_HOST = 'localhost'
#bucket1 = Bucket('couchbase://localhost/gs')
#rv1 = bucket1.get('__Files:40')
#pprint(rv1)

def get_data_bucket(data_bucket):
    from couchbase.bucket import Bucket
    return Bucket("couchbase://{0}/{1}".format(DATABASE_HOST, data_bucket), transcoder=ZlibTranscoder())

def _set(bucket, key, value, expire=0, must_not_exist=False, must_exist=False, cas=0):
    new_cas = None
    try:
        if must_exist:
        	result = bucket.replace(key, value.value, cas=cas, ttl=expire)
        elif must_not_exist:
            result = bucket.insert(key, value, ttl=expire)
        else:
            result = bucket.upsert(key, value.value)
        new_cas = result.cas
    except:
    	print("Unexpected error:", sys.exc_info()[0])
        new_cas = None
    return new_cas

for key in data:
	bucket_name = key
	print(key)
	bucket = get_data_bucket(bucket_name)
	for key2 in data[key]:
		rv = bucket.get(key2)
		_set(bucket, data[key][key2], bucket.get(key2), 0, False, False, 0)


