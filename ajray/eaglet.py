#!/usr/bin/env python
import json,copy
eagle = json.loads(open("eagle.json").read())
a = copy.deepcopy(eagle)
basic = ["int","char","string","real"]

# Yes this is generated at import time
# Yes I know it's evil to do this much processing at import time
types = {}
for atype,members in a.items():
  for member,memtype in members.items():
    if memtype not in basic and member != memtype:
      if member not in types:
        types[member] = memtype
      elif types[member] != memtype:
        print "Error, fatal assumption broken (any given member name has exactly one type)"
        exit(1)

header = """// json.ulp - Export an EagleCAD file into JSON
// Generated by the codez in this wonderful github repo:
// http://github.com/ajray/schematic-file-converter
// Alex Ray (2011) <ajray@ncsu.edu>
"""
misc = """
string esc(string s) { // JSON string escapes
    string out = "\\""; // open quote
    for (int i = 0; s[i]; ++i) {
        switch(s[i]) {
            case '"': out += "\\""; break;
            case '\\\\': out += "\\\\\\\\"; break;
            case '/': out += "\\\\/"; break;
            case '\\b': out += "\\\\b"; break;
            case '\\f': out += "\\\\f"; break;
            case '\\n': out += "\\\\n"; break;
            case '\\r': out += "\\\\r"; break;
            case '\\t': out += "\\\\t"; break;
            default: out += s[i];
        }
    }
    out += "\\""; // close quote
    return out;
}
void print__opener (string name) { // start of an object
  printf("\\"%s\\" : {\\n",name); 
}
void print__closer () { // end of an object
  printf("}\\n"); 
}
void pl(string a) { printf("%s:[",a); } // start of a list
void ln()         { printf("]"); }      // end of a list
void print_string (string a, string b)  { printf("%s:%s",a,esc(b)); }
void print_int    (string a, int b)     { printf("%s:%d",a,b); }
void print_real   (string a, real b)    { printf("%s:%g",esc(a),b); }
"""


