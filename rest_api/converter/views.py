# class ConverterBBoxJobViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = ConverterBBoxJob.objects.all()
#     serializer_class = ConverterBBoxJobSerializer
#
#     def perform_create(self, serializer):
#         result = self._start_conversion()
#         if result.status != 'failed':
#             serializer.status = ConversionProgress.RECEIVED
#             super().perform_create(serializer)
#
#     def _start_conversion(self):
#         bbox_job = self.get_object()
#         conversion_job = ConversionJobManager(geometry=BBox(*bbox_job.cut_out_area.extent))
#         conversion_job.start_conversion(callback_url='url')
#         return conversion_job
