from peekingduck.pipeline.nodes.dabble import bbox_count
from peekingduck.pipeline.nodes.draw import bbox, legend
from peekingduck.pipeline.nodes.model import yolo_face

class Detect_Face_Pipeline():
    def __init__(self):
        #Load the peeking duck nodes
        #Load yolo model
        self.yolo_face_node = yolo_face.Node()

        #Load bbox labeling method
        self.bbox_node = bbox.Node(show_labels=True)

        #Node to show info (OPTIONAL)
        #fps_node = fps.Node()
        self.count_node = bbox_count.Node()
        self.legend_node = legend.Node(show=["count"])

    def get_faces_and_bboxes(self, frame):
        #Process the frame to detect faces
        self.yolo_face_input = {'img': frame}
        self.yolo_face_output = self.yolo_face_node.run(self.yolo_face_input)

        #Get the bounding boxes
        self.bbox_input = {
            "img": frame,
            "bboxes": self.yolo_face_output["bboxes"],
            "bbox_labels": self.yolo_face_output["bbox_labels"], #'mask' or 'no mask'
        }

        #This draws the boxes on the image
        #Returns a useless (for now) array so just assign to that arbitrary variable
        _ = self.bbox_node.run(self.bbox_input)

        #Optional info stuff
        #fps_output = fps_node.run({"img": frame})
        count_output = self.count_node.run({"bboxes": self.yolo_face_output["bboxes"]})
        
        _ = self.legend_node.run({"img": frame, "count": count_output["count"]})


        #Get the number of faces detected
        num_bboxes = len(self.yolo_face_output['bboxes'])
        #num_bboxes = count_output['count'] #Alternative way
        #print(num_bboxes)

        bbox_labels = self.yolo_face_output['bbox_labels']

        #By default, alert is false
        no_mask_alert = False

        for label in bbox_labels:
            #print(label)
            if label == "no_mask":
                #If even one no_mask, alert
                no_mask_alert = True
                break

        #Return the frame and the number of faces detected
        return (num_bboxes, frame, no_mask_alert)

