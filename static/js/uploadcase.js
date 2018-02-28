/**
 * Created by python on 17-11-6.
 */

    $(function () {
        $(".file").change(function () {
            var file =$(".file").get(0).files[0];
            if (file) {
                var fileSize = 0;
                if (file.size > 1024 * 1024)
                    fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
                else
                    fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

                $(".filename").html(file.name);
                $(".filesize").html(fileSize);
                $(".filetype").html(file.type);
            }
        })
    });