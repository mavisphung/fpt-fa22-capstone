import React from 'react';
import { useState } from 'react';
import Dropzone, { IDropzoneProps } from 'react-dropzone-uploader';
import 'react-dropzone-uploader/dist/styles.css';
import { urlApi } from 'constants/UrlApi';
import { imageHeader, jsonHeaders, requestOption } from 'constants/HeadersRequest';
import { useHistory } from 'react-router-dom';
import { NotificationToast } from 'components/layout/NotificationToast';
import errorIcon from '../../../assets/images/error_icon.png';
import successIcon from '../../../assets/images/success_icon.png';

const CertificateUploader: React.FC<any> = (infoProps) => {
  const [renderTime, reRender] = useState(0);
  const history = useHistory();
  const [showToast, setShowToast] = React.useState(false);
  const [notification, setNotification] = React.useState({ icon: '', title: '', body: '' });

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
        for (let index = 0; index < urls.length; index++) {
          const url = urls[index];
          const fileRaw = files[index].file;
          requestOption.method = 'PUT';
          requestOption.headers = imageHeader;
          requestOption.body = fileRaw;
          await fetch(url, requestOption)
            .then((res) => res.url.slice(0, res.url.indexOf('?')))
            .then((imgUrl) => {
              infoProps.infoProps.specs.push({ url: imgUrl, ext: imgUrl.split('.').pop() });
            });
        }
        var infoRaw = JSON.stringify(infoProps.infoProps);
        requestOption.method = 'POST';
        requestOption.headers = jsonHeaders;
        requestOption.body = infoRaw;
        await fetch(urlApi + 'doctor/register/', requestOption).then((response) => {
          if (response.status === 201) {
            setShowToast(true);
            setNotification({
              icon: successIcon,
              title: 'Thành công',
              body: 'Mật khẩu sẽ được gửi qua mail sớm thôi!',
            });
            setTimeout(() => {
              history.replace('/login');
            }, 4000);
          } else {
            setShowToast(true);
            setNotification({
              icon: errorIcon,
              title: 'Không thành công',
              body: 'Vui lòng thử lại!',
            });
          }
        });
      })
      .catch((error) => console.log('error', error));

    allFiles.forEach((f) => f.remove());
    reRender(renderTime + 1);
  };

  return (
    <>
      <Dropzone
        getUploadParams={getUploadParams}
        onChangeStatus={handleChangeStatus}
        onSubmit={handleSubmit}
        accept="image/*"
        inputContent="Vui lòng tải lên ảnh chứng chỉ bác sĩ của bạn!"
        submitButtonContent="Đăng kí"
        styles={{ dropzone: { minHeight: 400, maxHeight: 500 } }}
      />
      <NotificationToast
        show={showToast}
        onClose={() => setShowToast(false)}
        content={notification}
      />
    </>
  );
};

export default CertificateUploader;
