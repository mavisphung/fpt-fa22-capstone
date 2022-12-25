import React from 'react';
import Dropzone, { IDropzoneProps } from 'react-dropzone-uploader';
import 'react-dropzone-uploader/dist/styles.css';
import { urlApi } from 'constants/UrlApi';
import { imageHeader, jsonHeaders, requestOption } from 'constants/HeadersRequest';
import CertificateUploader from './CertificateUploader';

const ImageUploader: React.FC<any> = (infoProps) => {
  const [tranferTime, goToUploadCerti] = React.useState(false);
  const [renderTime, reRender] = React.useState(0);

  // specify upload params and url for your files
  const getUploadParams: IDropzoneProps['getUploadParams'] = () => {
    reRender(renderTime + 1);
    return { url: 'https://httpbin.org/post' };
  };

  // called every time a file's `status` changes
  const handleChangeStatus: IDropzoneProps['onChangeStatus'] = () => {
    reRender(renderTime + 1);
  };

  // receives array of files that are done uploading when submit button is clicked
  const handleSubmit: IDropzoneProps['onSubmit'] = (files, allFiles) => {
    const arrFile = files.map((f) => ({
      ext: f.meta.name.split('.').pop(),
      size: Number(f.meta.size / (1024 * 1024)),
    }));

    var raw = JSON.stringify({
      images: arrFile,
    });

    requestOption.method = 'POST';
    requestOption.headers = jsonHeaders;
    requestOption.body = raw;

    fetch(urlApi + 'get-presigned-urls/', requestOption)
      .then((response) => response.json())
      .then((result) => result.data.urls)
      .then(async (urls) => {
        const url = urls[0];
        const fileRaw = files[0].file;
        requestOption.method = 'PUT';
        requestOption.headers = imageHeader;
        requestOption.body = fileRaw;
        await fetch(url, requestOption)
          .then((res) => res.url.slice(0, res.url.indexOf('?')))
          .then((avatarUrl) => {
            infoProps.infoProps.avatar = avatarUrl;
            files[0].remove();
            reRender(renderTime + 1);
            goToUploadCerti(true);
          });
      })
      .catch((error) => console.log('error', error));
  };

  return (
    <>
      {!tranferTime ? (
        <Dropzone
          getUploadParams={getUploadParams}
          onChangeStatus={handleChangeStatus}
          maxFiles={1}
          onSubmit={handleSubmit}
          accept="image/*"
          inputContent="Vui lòng tải lên 1 ảnh chân dung của bạn!"
          submitButtonContent="Đến cung cấp chứng chỉ bác sĩ của bạn"
          styles={{ dropzone: { height: 220 } }}
        />
      ) : (
        <CertificateUploader infoProps={infoProps.infoProps} />
      )}
    </>
  );
};

export default ImageUploader;
