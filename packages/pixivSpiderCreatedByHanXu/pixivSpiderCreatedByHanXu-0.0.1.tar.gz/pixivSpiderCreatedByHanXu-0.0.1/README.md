# Make sure that your internet can visit the foreign websites.
- The package has two modules to use.

# Module:keywordSpider
- The module can crawl the images based on the `keyword` you offered.
- Look at the following example:

```python
import pixivSpiderCreatedByHanXu.keywordSpider as kyS

if __name__ == '__main__':
    ex = kyS.pixiv_keyword_spider()
    ex()
```
```shell
type in the path where you want to reserve the images:Mio
type in the keywords used to search in pixiv:秋山澪
Type in the number of pages you want.Each page has almost 30 images:1
```
# Module:rankSpider
- The module can crawl the images based on the rank.
- You should offer date and mode. Look at the following example:

```python
import pixivSpiderCreatedByHanXu.rankSpider as rkS

if __name__ == '__main__':
    ex = rkS.pixiv_rank_spider
    ex()
```
```shell
{'1': 'daily', '2': 'weekly', '3': 'monthly', '4': 'rookie', '5': 'daily_ai', '6': 'male', '7': 'female'}
type in the searchMode you want1
Type in the date you want to search.Follow the format like this:2023042320221001
type in the path where you want to reserve the images:rank20221001
Type in the number of pages you want.Each page has almost 50 images:1
```
# Download
```shell

```