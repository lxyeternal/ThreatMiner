import sys
import pprint
from xml import etree
from gexf import Gexf

def create_gexf():

    main_path = "data/asset/data/"
    gexf_name = "test.gexf"
    whole_path = main_path + gexf_name
    out_file = open(whole_path,"wb")
    root = etree.SubElement("gexf")
    meta = etree.SubElement("meta",lastmodifieddate = "2018-10-12")


if __name__ == "__main__":

    create_gexf()