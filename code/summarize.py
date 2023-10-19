from math import remainder
from fpdf import FPDF
from PIL import Image

class PDF(FPDF):
    def header(self):
        self.set_fill_color(169, 204, 227)  # Background color for the entire top part
        self.rect(0, 0, 210, 25, 'DF')  # Draw a filled rectangle for the entire top part
        self.set_font('Arial', 'B', 16)  # Larger font for the header
        self.set_text_color(0, 0, 0)     # Text color: Black
        self.cell(0, 20, 'Dollar Bot Summary Report', 0, 1, 'C', 1)   # Centered title in the header
        #self.ln(15) 
        # Add a dollar sign logo to the top right corner of the header
        self.image('DollarBotLogo.png', 174, 0, 37)
        
        self.ln(20)  # Increase the space after the header

    def footer(self):
        self.set_font('Arial', 'I', 8)
        self.set_y(-15)
        
        self.set_text_color(0, 0, 0)  # Text color: Black
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

    def chapter_body(self, body, image_path):
        global y_after_his
        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "History report of your Spendings", ln=True, align='C')
        
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        y_position = self.get_y()
        self.set_fill_color(169,204,227)
        self.multi_cell(0, 10, body)
        #print(y_text_pos,"this is the y after text got inserted")
        # Get the current Y position
        
        y_text_pos = self.get_y()
        # Add the image (the .png image) on the right side of the history
        self.image(image_path, x=100, y=y_position, w=100)
        with Image.open(image_path) as img:
            height=img.height
        height = (height/300)*25.4
        print(height,"height of the history graph image")
        print(y_position+height,y_text_pos)
        if y_position+height> y_text_pos:
            y_after_his = y_position+height
        else:
            y_after_his = y_text_pos


    


    def chapter_displaybody(self, data, data_image):
        
        global max_height_lastImage
        #header_height = 25
        #footer_height = 15

        y_position = y_after_his+20  # Store the initial Y position
        #print(y_position)

        self.set_y(y_position+20)
        #print(self.get_y(),"hello")
        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Spending Report for the day", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, data[0])
        y_position=self.get_y()
        print(y_position,"this is after the first data")
        image_width=(self.w/2.2)
        #image_start=0
        
        for image_path in data_image[:3]:
            print(image_path)

        with Image.open(data_image[0]) as img:
            height1=img.height
        
        
        with Image.open(data_image[1]) as img:
            height2=img.height

        
        with Image.open(data_image[2]) as img:
            height3=img.height

        max_height=max(height1,height2)
        max_height=(max_height / 300) * 25.4

        height3 = (height3/300)*25.4
        
        self.set_y(self.get_y()+10)
        #print(max_height, self.h-20-35-self.get_y(),"first")
        if max_height> self.h-20-35-self.get_y():
            #print("entered the if condition")
            self.add_page()
            y_position=35
        
        self.image(data_image[0], x=10, y=y_position, w=image_width) 
        self.image(data_image[1], x=(image_width+10), y=y_position, w=image_width)

        self.set_y(self.get_y()+max_height+30)

        if height3 > self.h-20-35-self.get_y():
            self.add_page()
            y_position=35
        y_position=self.get_y()
        self.image(data_image[2], x=10, y=y_position, w=100)
        self.set_y(self.get_y()+max_height+35)
        

        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Spending Report for the month", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, data[1])
        y_position=self.get_y()
        
        with Image.open(data_image[3]) as img:
            height1=img.height
        
        
        with Image.open(data_image[4]) as img:
            height2=img.height

        
        with Image.open(data_image[5]) as img:
            height3=img.height

        max_height=max(height1,height2)
        max_height=(max_height / 300) * 25.4
        height3 = (height3/300)*25.4

        
        self.set_y(self.get_y()+10)
        #print(max_height,self.h-20-35-self.get_y(),"second")
        if max_height> self.h-20-35-self.get_y():
            #print("entered the if condition")
            self.add_page()
            y_position=35
        
        #print(self.get_y)
        self.image(data_image[3], x=10, y=y_position, w=image_width) 
        self.image(data_image[4], x=(image_width+10), y=y_position, w=image_width)

        self.set_y(self.get_y()+max_height+30)

        if height3 > self.h-20-35-self.get_y():
            self.add_page()
            y_position=35
        y_position=self.get_y()
        self.image(data_image[5], x=10, y=y_position, w=100)

        max_height_lastImage=max_height


            
    def chapter_estimatebody(self, data_day,data_month):
        self.set_y(self.get_y()+max_height_lastImage+30)

        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Estimation Report for the day", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        y_position=self.get_y()
        #print(data_day,data_month,"this is chapter_estimateody")

        self.multi_cell(0, 10, data_day[0])

        self.set_y(self.get_y()+20)
        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Spending Report for the month", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)

        self.multi_cell(0, 10, data_month[0])

    def chapter_asc_descbody(self,data_asc,data_desc):
        self.set_y(self.get_y()+20)
        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Spending Report in Ascending Order of Spent Amount", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)


        self.multi_cell(0, 10, data_asc)


        self.set_y(self.get_y()+20)
        self.set_font('Arial', 'BI', 12)  # Bold and italic
        self.set_text_color(0, 128, 0)  # Text color: Green
        self.cell(0, 10, "Spending Report in Descending Order of Spent Amount", ln=True, align='C')

        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)

        self.multi_cell(0, 10, data_desc)
