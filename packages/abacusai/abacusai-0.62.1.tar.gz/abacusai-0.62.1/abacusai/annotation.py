from .return_class import AbstractApiClass


class Annotation(AbstractApiClass):
    """
        An Annotation Store Annotation

        Args:
            client (ApiClient): An authenticated API Client instance
            annotationType (str): A name determining the type of annotation and how to interpret the annotation value data, e.g. as a label, bounding box, etc.
            annotationValue (dict): JSON-compatible value of the annotation. The format of the value is determined by the annotation type.
            comments (str): Comments about the annotation.
    """

    def __init__(self, client, annotationType=None, annotationValue=None, comments=None):
        super().__init__(client, None)
        self.annotation_type = annotationType
        self.annotation_value = annotationValue
        self.comments = comments

    def __repr__(self):
        return f"Annotation(annotation_type={repr(self.annotation_type)},\n  annotation_value={repr(self.annotation_value)},\n  comments={repr(self.comments)})"

    def to_dict(self):
        """
        Get a dict representation of the parameters in this class

        Returns:
            dict: The dict value representation of the class parameters
        """
        return {'annotation_type': self.annotation_type, 'annotation_value': self.annotation_value, 'comments': self.comments}
