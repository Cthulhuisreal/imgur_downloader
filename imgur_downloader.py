#! python3
import os
import requests
import bs4
new_download_links = []


def downloader(query, max_save, output_path):
    # create imgur search url
    query_url = 'https://imgur.com/search/?q=' + query
    # set up output_path
    abs_output_path = os.path.abspath(output_path)
    os.makedirs(abs_output_path, exist_ok=True)
    # Make request to imgur with query
    res1 = requests.get(query_url)
    try:
        res1.raise_for_status()
        # parse res.text with bs4 to images
        imgur_soup = bs4.BeautifulSoup(res1.text, 'html.parser')
        images = imgur_soup.select('.image-list-link img')
        # extract number image urls
        num_to_save = min(max_save, len(images))
        download_links = ['https:' + img.get('src') for img in images[:num_to_save]]
        for download_link in download_links:
            new_download_link = download_link.replace("b", "")
            new_download_links.append(new_download_link)
        # make requests for extracted url
        for link in new_download_links:
            # request image link from imgur
            res2 = requests.get(link)
            try:
                res2.raise_for_status()
                # save to file with url base name in folder results
                img_file = open(os.path.join(abs_output_path, os.path.basename(link)), 'wb')
                for chunk in res2.iter_content(100000):
                    img_file.write(chunk)
                img_file.close()
            except Exception as exc:
                print('There was a problem: %s' % exc)
    except Exception as exc:
        print('There was a problem: %s' % exc)
    print('Done!')


if __name__ == '__main__':
    downloader('kitties', 10, 'results')
