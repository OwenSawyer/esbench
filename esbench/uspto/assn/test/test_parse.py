# -*- coding: UTF-8 -*-

import datetime
import os.path
import unittest
import json

from .. import parse


ASSIGNMENT = """<patent-assignment><assignment-record><reel-no>29564</reel-no><frame-no>141</frame-no><last-update-date><date>20130104</date></last-update-date><purge-indicator>N</purge-indicator><recorded-date><date>20130103</date></recorded-date><page-count>6</page-count><correspondent><name>PERKINS COIE LLP</name><address-1>P.O. BOX 1247</address-1><address-2>PATENT - SEA</address-2><address-3>SEATTLE, WA 98111-1247</address-3></correspondent><conveyance-text>ASSIGNMENT OF ASSIGNORS INTEREST (SEE DOCUMENT FOR DETAILS).</conveyance-text></assignment-record><patent-assignors><patent-assignor><name>SCHMIDT, PETER</name><execution-date><date>20110812</date></execution-date></patent-assignor><patent-assignor><name>KEMPPAINEN, KURT</name><execution-date><date>20110812</date></execution-date></patent-assignor><patent-assignor><name>BASCHE, RAHN</name><execution-date><date>20110816</date></execution-date></patent-assignor></patent-assignors><patent-assignees><patent-assignee><name>WORDLOCK, INC.</name><address-1>2855 KIFER ROAD, SUITE 245</address-1><city>SANTA CLARA</city><state>CALIFORNIA</state><postcode>95051</postcode></patent-assignee></patent-assignees><patent-properties><patent-property><document-id><country>US</country><doc-number>29400306</doc-number><kind>X0</kind><date>20110825</date></document-id><document-id><country>US</country><doc-number>D662395</doc-number><kind>B1</kind><date>20120626</date></document-id><invention-title lang="en">COMBINATION DISC LOCK</invention-title></patent-property></patent-properties></patent-assignment>"""
PARSED = """{"_meta": {"parser_version": "0.0.1"}, "assignment_record": {"_rf": "29564_141", "conveyance_text": "ASSIGNMENT OF ASSIGNORS INTEREST (SEE DOCUMENT FOR DETAILS).", "correspondent": {"address": {"address_1": "P.O. BOX 1247", "address_2": "PATENT - SEA", "address_3": "SEATTLE, WA 98111-1247", "address_4": "", "city": "", "country": "", "postcode": "", "state": ""}, "name": "PERKINS COIE LLP"}, "date_last_update": "2013-01-04", "date_recorded": "2013-01-03", "frame_no": "141", "page_count": "6", "reel_no": "29564"}, "patent_assignees": [{"address": {"address_1": "2855 KIFER ROAD, SUITE 245", "address_2": "", "address_3": "", "address_4": "", "city": "SANTA CLARA", "country": "", "postcode": "95051", "state": "CALIFORNIA"}, "name": "WORDLOCK, INC."}], "patent_assignors": [{"address": {"address_1": "", "address_2": "", "address_3": "", "address_4": "", "city": "", "country": "", "postcode": "", "state": ""}, "date_execution": "2011-08-12", "name": "SCHMIDT, PETER"}, {"address": {"address_1": "", "address_2": "", "address_3": "", "address_4": "", "city": "", "country": "", "postcode": "", "state": ""}, "date_execution": "2011-08-12", "name": "KEMPPAINEN, KURT"}, {"address": {"address_1": "", "address_2": "", "address_3": "", "address_4": "", "city": "", "country": "", "postcode": "", "state": ""}, "date_execution": "2011-08-16", "name": "BASCHE, RAHN"}], "patent_properties": [{"doc_ids": [{"_type": "APP", "country": "US", "date": "2011-08-25", "doc_number": "29400306", "kind": "X0"}, {"_type": "PAT", "country": "US", "date": "2012-06-26", "doc_number": "D662395", "kind": "B1"}], "invention_title": "COMBINATION DISC LOCK", "invention_title_lang": "EN"}], "patent_properties_count": 1}"""

LONG_XML = """<patent-assignment><assignment-record><reel-no>29554</reel-no><frame-no>84</frame-no><last-update-date><date>20130104</date></last-update-date><purge-indicator>N</purge-indicator><recorded-date><date>20121231</date></recorded-date><page-count>16</page-count><correspondent><name>LATHAM &amp; WATKINS LLP</name><address-1>650 TOWN CENTER DRIVE, 20TH FLOOR</address-1><address-2>COSTA MESA, CA 92626</address-2></correspondent><conveyance-text>RELEASE OF SECURITY INTEREST IN PATENT COLLATERAL AT REEL/FRAME NO.027803/0850</conveyance-text></assignment-record><patent-assignors><patent-assignor><name>U.S. BANK NATIONAL ASSOCIATION</name><execution-date><date>20121231</date></execution-date></patent-assignor></patent-assignors><patent-assignees><patent-assignee><name>SAN JAMAR, INC.</name><address-1>555 KOOPMAN LANE</address-1><city>ELKHORN</city><state>WISCONSIN</state><postcode>53121-2012</postcode></patent-assignee></patent-assignees><patent-properties><patent-property><document-id><country>US</country><doc-number>10594942</doc-number><kind>X0</kind><date>20060928</date></document-id><document-id><country>US</country><doc-number>20070193302</doc-number><kind>A1</kind><date>20070823</date></document-id><invention-title lang="en">Chilling Utensil and Method of Use</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12489192</doc-number><kind>X0</kind><date>20090622</date></document-id><document-id><country>US</country><doc-number>20090255942</doc-number><kind>A1</kind><date>20091015</date></document-id><invention-title lang="en">Container</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12145954</doc-number><kind>X0</kind><date>20080625</date></document-id><document-id><country>US</country><doc-number>20090057334</doc-number><kind>A1</kind><date>20090305</date></document-id><invention-title lang="en">CUP DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12207063</doc-number><kind>X0</kind><date>20080909</date></document-id><document-id><country>US</country><doc-number>20090008851</doc-number><kind>A1</kind><date>20090108</date></document-id><document-id><country>US</country><doc-number>8286956</doc-number><kind>B2</kind><date>20121016</date></document-id><invention-title lang="en">CUTTING BOARD AND STAND</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12739331</doc-number><kind>X0</kind><date>20100624</date></document-id><document-id><country>US</country><doc-number>20110133010</doc-number><kind>A1</kind><date>20110609</date></document-id><invention-title lang="en">DISCRIMINATING WEB MATERIAL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11908390</doc-number><kind>X0</kind><date>20100219</date></document-id><document-id><country>US</country><doc-number>20100187248</doc-number><kind>A1</kind><date>20100729</date></document-id><invention-title lang="en"> DISPENSER FOR LIDS</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12297135</doc-number><kind>X0</kind><date>20081014</date></document-id><document-id><country>US</country><doc-number>20100030376</doc-number><kind>A1</kind><date>20100204</date></document-id><invention-title lang="en">EXCLUSIVITY SYSTEM AND METHOD</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29376379</doc-number><kind>X0</kind><date>20101006</date></document-id><document-id><country>US</country><doc-number>D656382</doc-number><kind>B1</kind><date>20120327</date></document-id><invention-title lang="en">HANDLE FOR TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12694040</doc-number><kind>X0</kind><date>20100126</date></document-id><document-id><country>US</country><doc-number>20100187242</doc-number><kind>A1</kind><date>20100729</date></document-id><invention-title lang="en">Ice Tote Having a Hanging Device</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>13125406</doc-number><kind>X0</kind><date>20110914</date></document-id><document-id><country>US</country><doc-number>20120109366</doc-number><kind>A1</kind><date>20120503</date></document-id><invention-title lang="en">INSERT FOR USE WITH A ROLL OF WEB MATERIAL, AND PROVIDING A UNIQUE IDENTIFIER FOR THE ROLL OF WEB MATERIAL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>13142112</doc-number><kind>X0</kind><date>20110624</date></document-id><document-id><country>US</country><doc-number>20120181371</doc-number><kind>A1</kind><date>20120719</date></document-id><invention-title lang="en">Roll Dispenser</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>12162456</doc-number><kind>X0</kind><date>20110714</date></document-id><document-id><country>US</country><doc-number>20110259949</doc-number><kind>A1</kind><date>20111027</date></document-id><invention-title lang="en">Solid Food Product Container Dispenser</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29404060</doc-number><kind>X0</kind><date>20111014</date></document-id><document-id><country>US</country><doc-number>D665206</doc-number><kind>B1</kind><date>20120814</date></document-id><invention-title lang="en">TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11438192</doc-number><kind>X0</kind><date>20060522</date></document-id><document-id><country>US</country><doc-number>20070034320</doc-number><kind>A1</kind><date>20070215</date></document-id><invention-title lang="en">Wrap dispensing station and method</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>09391555</doc-number><kind>X0</kind><date>19990908</date></document-id><document-id><country>US</country><doc-number>6199723</doc-number><kind>B1</kind><date>20010313</date></document-id><invention-title lang="en">APPARATUS FOR HOLDING A CUP IN A CUP DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29187252</doc-number><kind>X0</kind><date>20030729</date></document-id><document-id><country>US</country><doc-number>D522241</doc-number><kind>B1</kind><date>20060606</date></document-id><invention-title lang="en">CARRYING DEVICE</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29197570</doc-number><kind>X0</kind><date>20040116</date></document-id><document-id><country>US</country><doc-number>D577041</doc-number><kind>B1</kind><date>20080916</date></document-id><invention-title lang="en">CHILLING UTENSIL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29243284</doc-number><kind>X0</kind><date>20051122</date></document-id><document-id><country>US</country><doc-number>D550724</doc-number><kind>B1</kind><date>20070911</date></document-id><invention-title lang="en">CHILLING UTENSIL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29243285</doc-number><kind>X0</kind><date>20051122</date></document-id><document-id><country>US</country><doc-number>D550089</doc-number><kind>B1</kind><date>20070904</date></document-id><invention-title lang="en">CHILLING UTENSIL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29189042</doc-number><kind>X0</kind><date>20030827</date></document-id><document-id><country>US</country><doc-number>D496233</doc-number><kind>B1</kind><date>20040921</date></document-id><invention-title lang="en">COMBINED SCOOP AND SHEATH</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29190371</doc-number><kind>X0</kind><date>20030919</date></document-id><document-id><country>US</country><doc-number>D507460</doc-number><kind>B1</kind><date>20050719</date></document-id><invention-title lang="en">CONDIMENT DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29138317</doc-number><kind>X0</kind><date>20010309</date></document-id><document-id><country>US</country><doc-number>D462240</doc-number><kind>B1</kind><date>20020903</date></document-id><invention-title lang="en">CONDIMENT DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29258300</doc-number><kind>X0</kind><date>20060419</date></document-id><document-id><country>US</country><doc-number>D563180</doc-number><kind>B1</kind><date>20080304</date></document-id><invention-title lang="en">CUTTING BOARD</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29209355</doc-number><kind>X0</kind><date>20040714</date></document-id><document-id><country>US</country><doc-number>D512281</doc-number><kind>B1</kind><date>20051206</date></document-id><invention-title lang="en">CUTTING BOARD</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29173563</doc-number><kind>X0</kind><date>20021231</date></document-id><document-id><country>US</country><doc-number>D507463</doc-number><kind>B1</kind><date>20050719</date></document-id><invention-title lang="en">CUTTING BOARD</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11438646</doc-number><kind>X0</kind><date>20060522</date></document-id><document-id><country>US</country><doc-number>20070001359</doc-number><kind>A1</kind><date>20070104</date></document-id><document-id><country>US</country><doc-number>7422201</doc-number><kind>B2</kind><date>20080909</date></document-id><invention-title lang="en">CUTTING BOARD AND STAND</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29260219</doc-number><kind>X0</kind><date>20060522</date></document-id><document-id><country>US</country><doc-number>D574200</doc-number><kind>B1</kind><date>20080805</date></document-id><invention-title lang="en">CUTTING STATION</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29322466</doc-number><kind>X0</kind><date>20080805</date></document-id><document-id><country>US</country><doc-number>D605908</doc-number><kind>B1</kind><date>20091215</date></document-id><invention-title lang="en">CUTTING STATION</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29220407</doc-number><kind>X0</kind><date>20041230</date></document-id><document-id><country>US</country><doc-number>D525063</doc-number><kind>B1</kind><date>20060718</date></document-id><invention-title lang="en">DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29220406</doc-number><kind>X0</kind><date>20041230</date></document-id><document-id><country>US</country><doc-number>D525465</doc-number><kind>B1</kind><date>20060725</date></document-id><invention-title lang="en">DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29220405</doc-number><kind>X0</kind><date>20041230</date></document-id><document-id><country>US</country><doc-number>D522784</doc-number><kind>B1</kind><date>20060613</date></document-id><invention-title lang="en">DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29186425</doc-number><kind>X0</kind><date>20030715</date></document-id><document-id><country>US</country><doc-number>D493312</doc-number><kind>B1</kind><date>20040727</date></document-id><invention-title lang="en">DISPENSER FACE PLATE</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11813144</doc-number><kind>X0</kind><date>20071112</date></document-id><document-id><country>US</country><doc-number>20080190982</doc-number><kind>A1</kind><date>20080814</date></document-id><document-id><country>US</country><doc-number>7931228</doc-number><kind>B2</kind><date>20110426</date></document-id><invention-title lang="en">DISPENSER FOR SHEET MATERIAL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>09959251</doc-number><kind>X0</kind><date>20020129</date></document-id><document-id><country>US</country><doc-number>7044421</doc-number><kind>B1</kind><date>20060516</date></document-id><invention-title lang="en">ELECTRONICALLY CONTROLLED ROLL TOWEL DISPENSER WITH DATA COMMUNICATION SYSTEM</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29228818</doc-number><kind>X0</kind><date>20050428</date></document-id><document-id><country>US</country><doc-number>D579249</doc-number><kind>B1</kind><date>20081028</date></document-id><invention-title lang="en">FACEPLATE</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29241214</doc-number><kind>X0</kind><date>20051025</date></document-id><document-id><country>US</country><doc-number>D546604</doc-number><kind>B1</kind><date>20070717</date></document-id><invention-title lang="en">FACEPLATE</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>09392187</doc-number><kind>X0</kind><date>19990909</date></document-id><document-id><country>US</country><doc-number>6315155</doc-number><kind>B1</kind><date>20011113</date></document-id><invention-title lang="en">FOLDED PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>09748521</doc-number><kind>X0</kind><date>20001222</date></document-id><document-id><country>US</country><doc-number>20010020624</doc-number><kind>A1</kind><date>20010913</date></document-id><document-id><country>US</country><doc-number>6543641</doc-number><kind>B2</kind><date>20030408</date></document-id><invention-title lang="en">FOLDED PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29225537</doc-number><kind>X0</kind><date>20050317</date></document-id><document-id><country>US</country><doc-number>D602203</doc-number><kind>B1</kind><date>20091013</date></document-id><invention-title lang="en">HAND AND NAIL BRUSH</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29138268</doc-number><kind>X0</kind><date>20010309</date></document-id><document-id><country>US</country><doc-number>D471062</doc-number><kind>B1</kind><date>20030304</date></document-id><invention-title lang="en">LID FOR CONDIMENT DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29172919</doc-number><kind>X0</kind><date>20021218</date></document-id><document-id><country>US</country><doc-number>D488654</doc-number><kind>B1</kind><date>20040420</date></document-id><invention-title lang="en">LOW COST ROLL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29259510</doc-number><kind>X0</kind><date>20060510</date></document-id><document-id><country>US</country><doc-number>D571834</doc-number><kind>B1</kind><date>20080624</date></document-id><invention-title lang="en">MANDREL FOR HOLDING ROLLS OF WEB MATERIAL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>08340705</doc-number><kind>X0</kind><date>19941116</date></document-id><document-id><country>US</country><doc-number>5478404</doc-number><kind>B1</kind><date>19951226</date></document-id><invention-title lang="en">METHOD FOR CLEANING THE BLADE OF A FOOD PRODUCT SLICING MACHINE</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>10891429</doc-number><kind>X0</kind><date>20040714</date></document-id><document-id><country>US</country><doc-number>20050150898</doc-number><kind>A1</kind><date>20050714</date></document-id><document-id><country>US</country><doc-number>7543719</doc-number><kind>B2</kind><date>20090609</date></document-id><invention-title lang="en">NAPKIN DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29325053</doc-number><kind>X0</kind><date>20080925</date></document-id><document-id><country>US</country><doc-number>D590213</doc-number><kind>B1</kind><date>20090414</date></document-id><invention-title lang="en">NAPKIN HOLDER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29337161</doc-number><kind>X0</kind><date>20090515</date></document-id><document-id><country>US</country><doc-number>D608066</doc-number><kind>B1</kind><date>20100112</date></document-id><invention-title lang="en">PAIL</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29097725</doc-number><kind>X0</kind><date>19981211</date></document-id><document-id><country>US</country><doc-number>D419014</doc-number><kind>B1</kind><date>20000118</date></document-id><invention-title lang="en">PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29097685</doc-number><kind>X0</kind><date>19981211</date></document-id><document-id><country>US</country><doc-number>D419805</doc-number><kind>B1</kind><date>20000201</date></document-id><invention-title lang="en">PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29127989</doc-number><kind>X0</kind><date>20000816</date></document-id><document-id><country>US</country><doc-number>D457368</doc-number><kind>B1</kind><date>20020521</date></document-id><invention-title lang="en">PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29153706</doc-number><kind>X0</kind><date>20011108</date></document-id><document-id><country>US</country><doc-number>D461983</doc-number><kind>B1</kind><date>20020827</date></document-id><invention-title lang="en">PAPER TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29134812</doc-number><kind>X0</kind><date>20001229</date></document-id><document-id><country>US</country><doc-number>D452788</doc-number><kind>B1</kind><date>20020108</date></document-id><invention-title lang="en">Plastic film dispenser</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>10339194</doc-number><kind>X0</kind><date>20030109</date></document-id><document-id><country>US</country><doc-number>20040135028</doc-number><kind>A1</kind><date>20040715</date></document-id><document-id><country>US</country><doc-number>7168653</doc-number><kind>B2</kind><date>20070130</date></document-id><invention-title lang="en">LOW COST ROLL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>10945688</doc-number><kind>X0</kind><date>20040921</date></document-id><document-id><country>US</country><doc-number>20050151384</doc-number><kind>A1</kind><date>20050714</date></document-id><document-id><country>US</country><doc-number>7621572</doc-number><kind>B2</kind><date>20091124</date></document-id><invention-title lang="en">SCOOP AND SHEATH</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29151472</doc-number><kind>X0</kind><date>20011108</date></document-id><document-id><country>US</country><doc-number>D458495</doc-number><kind>B1</kind><date>20020611</date></document-id><invention-title lang="en">SOAP DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29087254</doc-number><kind>X0</kind><date>19980429</date></document-id><document-id><country>US</country><doc-number>D405661</doc-number><kind>B1</kind><date>19990216</date></document-id><invention-title lang="en">SPATULA</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11372627</doc-number><kind>X0</kind><date>20060310</date></document-id><document-id><country>US</country><doc-number>20060203878</doc-number><kind>A1</kind><date>20060914</date></document-id><document-id><country>US</country><doc-number>7455451</doc-number><kind>B2</kind><date>20081125</date></document-id><invention-title lang="en">TEST STRIP DISPENSER AND THERMOMETER HOLDER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29151569</doc-number><kind>X0</kind><date>20011108</date></document-id><document-id><country>US</country><doc-number>D457766</doc-number><kind>B1</kind><date>20020528</date></document-id><invention-title lang="en">TOILET PAPER DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29151464</doc-number><kind>X0</kind><date>20011108</date></document-id><document-id><country>US</country><doc-number>D458489</doc-number><kind>B1</kind><date>20020611</date></document-id><invention-title lang="en">TOILET PAPER DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29151606</doc-number><kind>X0</kind><date>20011108</date></document-id><document-id><country>US</country><doc-number>D458490</doc-number><kind>B1</kind><date>20020611</date></document-id><invention-title lang="en">TOILET PAPER DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29376404</doc-number><kind>X0</kind><date>20101006</date></document-id><document-id><country>US</country><doc-number>D637841</doc-number><kind>B1</kind><date>20110517</date></document-id><invention-title lang="en">TOWEL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29088628</doc-number><kind>X0</kind><date>19980528</date></document-id><document-id><country>US</country><doc-number>D411677</doc-number><kind>B1</kind><date>19990629</date></document-id><invention-title lang="en">TRASH CAN TABLEWARE  RETRIEVER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>11839231</doc-number><kind>X0</kind><date>20070815</date></document-id><document-id><country>US</country><doc-number>20080042006</doc-number><kind>A1</kind><date>20080221</date></document-id><document-id><country>US</country><doc-number>7641143</doc-number><kind>B2</kind><date>20100105</date></document-id><invention-title lang="en">WEB MATERIAL DISPENSER</invention-title></patent-property><patent-property><document-id><country>US</country><doc-number>29260226</doc-number><kind>X0</kind><date>20060522</date></document-id><document-id><country>US</country><doc-number>D573619</doc-number><kind>B1</kind><date>20080722</date></document-id><invention-title lang="en">WRAP DISPENSING STATION</invention-title></patent-property></patent-properties></patent-assignment>"""
LONG_PARSED = ""

class ParseTest(unittest.TestCase):

    def test_PatentAssignment(self):
        ar = parse.PatentAssignment(ASSIGNMENT)
        s = json.dumps(ar, indent=None, sort_keys=True)        
        self.assertEqual(s, PARSED)


    def test_format_date(self):
        self.assertEqual('2010-01-01', parse.format_date('20100101'))
        self.assertEqual('', parse.format_date('foo'))
    
    
    def test_metadata(self): 
        self.assertEqual({'parser_version': '0.0.1', 'googl_date_published': '2010-11-02', 'googl_type': 'frontside', 'googl_filename': 'ad20101102.xml'}, parse.metadata('ad20101102.xml'))
        self.assertEqual({'parser_version': '0.0.1', 'googl_date_published': '2010-11-02', 'googl_type': 'frontside', 'googl_filename': 'ad20101102.xml'}, parse.metadata('/foo/foo/ad20101102.xml'))
        self.assertEqual({'parser_version': '0.0.1', 'googl_date_published': '2010-11-02', 'googl_type': 'backside', 'googl_filename': 'ad20101102-01.xml'}, parse.metadata('ad20101102-01.xml'))
        self.assertEqual({'parser_version': '0.0.1'}, parse.metadata(''))
        self.assertEqual({'parser_version': '0.0.1'}, parse.metadata(None))

        
if __name__ == "__main__":
    unittest.main()     

