# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapywork.models import mysqldb
from scrapywork.models import hfs



from urllib.request import urlretrieve
from scrapy.pipelines.images import ImagesPipeline
from PIL import Image
from io import BytesIO
from scrapy.pipelines.files import FileException
import six
import logging

class ArticlePipeline(object):
    def process_item(self,item,spider):
        try:
            self._mysqldb_insertitem(item)

            logging.info(item)
            return item
        except:
            raise DropItem('Cannot Insert %s into mysql database'% item)
            logging.info('db error')

    def _parse_sourceandhtml(self,images,files,html):
        source=[]
        htmlreplace=html
        for image in images:
            logging.info(image)
            imagename = image['path'].split('/')[-1]
            htmlreplace = htmlreplace.replace(str(image['url']), str(imagename))
            source.append(imagename)
            hfs.UploadStreamXImages(imagename)
        for file in files:
            logging.info(file)
            filename = file['path'].split('/')[-1]
            htmlreplace = htmlreplace.replace(str(file['url']),str(filename))
            source.append(filename)
            hfs.UploadStreamXFiles(filename)
        return '|'.join(source),htmlreplace

    def _mysqldb_insertitem(self,item):
        sources, html = self._parse_sourceandhtml(item['images'], item['files'], item['html'])
        time = item['time']


        mysqldb.insertItem(url=item['url'],site=item['site'],title=item['title'],time=time,type=item['type'],publish=item['publish'],
                           html=html,text=item['text'],xml=item['xml'],sources=sources)


import tempfile
import cv2
class OptimizeImagesPipeline(ImagesPipeline):

    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)

        try:
            orig_image = Image.open(BytesIO(response.body))
        except IOError:
            tempimage=tempfile.gettempdir()+'\\'+path.split('.')[0].split('/')[-1]+'.png'
            urlretrieve(request.url,tempimage)
            image = cv2.imread(tempimage)
            cv2.imwrite(tempimage, image)
            orig_image=Image.open(tempimage)

        width, height = orig_image.size

        if width < self.min_width or height < self.min_height:
            raise FileException("Image too small (%dx%d < %dx%d)" %
                                        (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield path, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf
