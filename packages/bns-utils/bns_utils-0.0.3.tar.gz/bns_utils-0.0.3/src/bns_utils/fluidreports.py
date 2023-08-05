import re
import xml.etree.ElementTree as ET

class Report:
    def __init__(self,dir):
        self.dir = dir
        with open(dir,"r") as f:
            txt = f.read()
        #Get report id
        id_pat = re.compile("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}")
        self.id = id_pat.search(txt).group()
        #Get datasources
        datasource_xml_seperator_pat = "<!!!>\n{0,1}"
        data_sources_pat = re.compile("----- DataSource Parameter Containers -----\n([\S\n\t\v ]*?)\n----- .* -----")
        self.data_source_list = re.split(datasource_xml_seperator_pat,data_sources_pat.search(txt).group(1))
        #Get calcs
        self.calc_list = []
        calc_pat = re.compile("----- CalculationSource Parameter Containers -----\n([\S\n\t\v ]*?)\n----- .* -----")
        calcs_xml_seperator_pat = "\n{0,1}<------Calculation Source------>\n{0,1}"
        calc_type_pat = re.compile("<CalculationClass_FullName>(.*?)</CalculationClass_FullName>\n")
        calc_part_pat = re.compile("<!!!!!>")
        for calc in re.split(calcs_xml_seperator_pat,calc_pat.search(txt).group(1)):
            if calc == "":
                continue
            else:
                calc_attrib_dict = {"CalculationClass_FullName":calc_type_pat.search(calc).group(1)}
                calc_parts = re.split(calc_part_pat,re.sub(calc_type_pat,"",calc))
                self.calc_list.append((calc_attrib_dict,calc_parts))
        #Get post filter
        self.postfilter_list = []
        postfilter_pat = re.compile("----- PostFilter Parameter Containers -----\n([\S\n\t\v ]*?)\n----- .* -----")
        postfilter_sep_pat = re.compile("[\n]{0,1}<------Post Filter------>[\n]{0,1}")
        postfilter_type_pat = re.compile("<PostFilterClass_FullName>(.*)</.*>")
        postfilter_parts_sep_pat = re.compile("[\n]{0,1}<!!!!!>[\n]{0,1}")
        postfilter_txt = postfilter_pat.search(txt).group(1)
        for postfilter in re.split(postfilter_sep_pat,postfilter_txt):
            if postfilter == "":
                continue
            else:
                postfilter_attrib_dict = {"PostFilterClass_FullName":postfilter_type_pat.search(postfilter).group(1)}
                postfilter_parts = re.split(postfilter_parts_sep_pat,re.sub(postfilter_type_pat,"",postfilter))
                self.postfilter_list.append((postfilter_attrib_dict,postfilter_parts))
        #Get scheduling
        schedule_pat = re.compile("----- Scheduler Parameter Container -----\n([\S\n\t\v ]*?)\n----- .* -----")
        self.schedule = schedule_pat.search(txt).group(1)
        #Get mapping      
        mapping_pat = re.compile("----- Mapping Container -----\n([\S\n\t\v ]*?)\n----- .* -----")
        self.mapping = mapping_pat.search(txt).group(1)
        #Get design
        self.design_list = []
        design_pat = re.compile("----- Report Design -----\n([\S\n\t\v ]*?)\n----- .* -----")
        design_txt = design_pat.search(txt).group(1)
        design_row_pat = re.compile("[\n]{0,1}<------Design Row------>[\n]{0,1}")
        design_plot_pat = re.compile("[\n]{0,1}<------Design Plot------->[\n]{0,1}")
        row_attribs_pat = re.compile("<(.*)>(.*)</.*>")
        for row in re.split(design_row_pat,design_txt):
            if row == "":
                continue
            row_attrib_dict = {}
            row_plots = []
            for count,plot in enumerate(re.split(design_plot_pat,row)):
                if count == 0:
                    for attrib in row_attribs_pat.finditer(plot):
                        row_attrib_dict[attrib.group(1)] = attrib.group(2)
                else:
                    row_plots.append(plot)
            self.design_list.append((row_attrib_dict,row_plots))            
        #Get transmission
        self.transmission_list = []
        transmission_pat = re.compile("----- Transmission Container -----\n([\S\n\t\v ]*?)\n----- .* -----")
        transmission_sep_pat = re.compile("[\n]{0,1}<------Transmitter------>[\n]{0,1}")
        transmitter_sep_pat = re.compile("[\n]{0,1}<!!!!!>[\n]{0,1}")
        transmitter_type_pat = re.compile("<TransmitterClass_FullName>(.*)</.*>")
        transmission_txt = transmission_pat.search(txt).group(1)
        for transmitter in re.split(transmission_sep_pat,transmission_txt):            
            if transmitter == "":
                continue
            else:
                transmitter_attrib_dict = {"TransmitterClass_FullName":transmitter_type_pat.search(transmitter).group(1)}
                transmitter_parts = re.split(transmitter_sep_pat,re.sub(transmitter_type_pat,"",transmitter))
                self.transmission_list.append((transmitter_attrib_dict,transmitter_parts))
                    
    def datasource_tags(self,add_affix = False,add_constant = False):
        report_tags = []
        for data_source_txt in self.data_source_list:
            root = ET.fromstring(data_source_txt)
            data_source_type = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
            data_source_affix=None
            for affix in root.iter('TagAffix'):
                data_source_affix = affix.text
            if add_constant or data_source_type != "ConstantDataSourceParameters":
                for tags in root.iter('Tags'):
                    for tag in tags:
                        if not add_affix:
                            if data_source_affix == None:
                                report_tags.append(tag.text)
                            else:
                                report_tags.append(tag.text[:-len(data_source_affix)])
                        else:
                            report_tags.append(tag.text)
        ## Return unique list!!!
        return report_tags
    
    def calcs_input_tags(self):
        input_tags =[]
        for calc_obj in self.calc_list:
            calc_tags = []            
            root = ET.fromstring(calc_obj[1][0])
            for xml_tag in root.iter('Name'):
                calc_name = xml_tag.text
            for tags in root.iter('InputDataPoints'):
                for tag in tags:
                    calc_tags.append(tag.text)
            input_tags.append((calc_name,calc_tags))
        return input_tags

    def calcs_output_tags(self):
        output_tags =[]
        for calc_obj in self.calc_list:
            calc_tags = []            
            root = ET.fromstring(calc_obj[1][0])
            for xml_tag in root.iter('Name'):
                calc_name = xml_tag.text
            for tags in root.iter('OutputDataPoints'):
                for tag in tags:
                    calc_tags.append(tag.text)
            output_tags.append((calc_name,calc_tags))
        return output_tags

    def mapping_tags(self):
        mapping_tags = []
        root = ET.fromstring(self.mapping)
        for tag in root.iter('InputName'):
            mapping_tags.append(tag.text)
        return mapping_tags
    
    def schedule_type(self):
        root = ET.fromstring(self.schedule)
        for schedule_type in root.findall("{fluidReports}ScheduleType"):
            return schedule_type.text
        
    def get_mail_list(self):
        mail_list = []
        for transmitter in self.transmission_list:
            t_type = transmitter[0]['TransmitterClass_FullName']
            print(transmitter[1][0])
            test = ET.fromstring(transmitter[1][0])
            if t_type == "fluidReports.Transmission.Email.Transmission_Email":
                root = ET.fromstring(transmitter[1][1])
                for recipients in root.iter("Recipients"):
                    for recipient in recipients:
                        mail_list.append(recipient.text)
        return mail_list

    def rebuild(self, filename):
        report_txt = ""
        #build id
        id_header = "----- Report Id -----\n"
        report_txt += id_header
        report_txt += self.id
        #build datasources
        datasource_header = "\n----- DataSource Parameter Containers -----\n"
        report_txt += datasource_header
        for count,datasource in enumerate(self.data_source_list):
            if count < len(self.data_source_list)-1:
                append_str = "<!!!>\n"
            else:
                append_str = ""
            report_txt += datasource + append_str
        #build calcs
        report_txt += "\n----- CalculationSource Parameter Containers -----\n"
        calc_sep = "<------Calculation Source------>\n"
        for calc_obj in self.calc_list:
            report_txt += calc_sep
            for key in calc_obj[0]:
                value = calc_obj[0][key]
                attrib_str = f"<{key}>{value}</{key}>\n"
                report_txt += attrib_str
            report_txt += calc_obj[1][0]
            report_txt += "<!!!!!>"
            report_txt += calc_obj[1][1]
        #build postfilter
        report_txt += "\n----- PostFilter Parameter Containers -----\n"
        postfilter_sep = "<------Post Filter------>\n"
        for postfilter_obj in self.postfilter_list:
            report_txt += postfilter_sep
            for key in postfilter_obj[0]:
                value = postfilter_obj[0][key]
                attrib_str = f"<{key}>{value}</{key}>"
                report_txt += attrib_str
            report_txt += postfilter_obj[1][0]
            report_txt += "<!!!!!>"
            report_txt += postfilter_obj[1][1]
        #build scheduler
        report_txt += "\n----- Scheduler Parameter Container -----\n"
        report_txt += self.schedule
        #build mapping
        report_txt += "\n----- Mapping Container -----\n"
        report_txt += self.mapping
        #build design
        report_txt += "\n----- Report Design -----\n"
        row_sep = "<------Design Row------>\n"
        design_sep = "<------Design Plot------->\n"
        for row_obj in self.design_list:
            report_txt += row_sep
            for key in row_obj[0]:
                value = row_obj[0][key]
                attrib_str = f"<{key}>{value}</{key}>\n"
                report_txt += attrib_str
            #print(row_obj[1])
            for plot in row_obj[1]:
                report_txt += design_sep
                report_txt += plot
        #build transmission
        report_txt += "----- Transmission Container -----\n"
        transmission_sep = "<------Transmitter------>\n"
        for transmission_obj in self.transmission_list:
            report_txt += transmission_sep
            for key in transmission_obj[0]:
                value = transmission_obj[0][key]
                attrib_str = f"<{key}>{value}</{key}>"
                report_txt += attrib_str
            report_txt += transmission_obj[1][0]
            report_txt += "<!!!!!>"
            report_txt += transmission_obj[1][1]
        #build end
        report_txt += "\n----- Logger Folder -----\nDiscontinued\n----- Logger Prefix -----\nDiscontinued"
        
        #write to file
        with open(filename, 'w') as f:
            f.write(report_txt)

    def clean(self, filename):
        #remove unused calc
        delete_list = []
        calc_output_tags = self.calcs_output_tags()
        mapping_tags = self.mapping_tags()
        for calc in calc_output_tags:
            delete_flag = False
            for tag in calc[1]:
                if tag in mapping_tags:
                    delete_flag = False
                    break
                else:
                    delete_flag = True
            if delete_flag:
                delete_list.append(calc[0])
        calcs_that_stay = []
        for calc_obj in self.calc_list:
            root = ET.fromstring(calc_obj[1][0])
            for name_tag in root.iter('Name'):
                calc_name = name_tag.text
                if not calc_name in delete_list:
                    calcs_that_stay.append(calc_obj)
        self.calc_list = calcs_that_stay
        #remove unused calc tags (does not check script calcs)
        #remove unused tags from datasources
        used_tags = self.mapping_tags()
        for input_calc_tags in self.calcs_input_tags():
            used_tags.extend(input_calc_tags[1])
        used_tags = list(set(used_tags))
        new_source_list = []
        removed_tags = []
        for source in self.data_source_list:
            index_removed = []
            root = ET.fromstring(source)
            tags_xml = root.find('Tags')
            for count,tag in enumerate(tags_xml.findall('string')):
                if not tag.text in used_tags:
                    index_removed.append(count)
                    removed_tags.append(tag.text)
                    tags_xml.remove(tag)
            ##check for values and delete
            if root.find("Values"):
                values_xml = root.find('Values')
                for count,value in enumerate(values_xml.findall('double')):
                    if count in index_removed:
                        values_xml.remove(value)
            ##check for trimmed tags and delete
            if root.find("TrimmedTags"):
                trimmed_xml = root.find('TrimmedTags')
                for count,trimmed in enumerate(trimmed_xml.findall('string')):
                    if count in index_removed:
                        trimmed_xml.remove(trimmed)
            new_source_list.append(ET.tostring(root,encoding="unicode"))
        self.data_source_list = new_source_list
        #write clean report
        self.rebuild(filename)