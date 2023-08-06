import os
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class LicenseIdentifier:
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        self.cache_file = os.path.join(
                            self.cache_dir,
                            'license_identifier.pkl')
        self.vectorizer = None
        self.classifier = None

        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                self.vectorizer, self.classifier = pickle.load(f)
        else:
            self.license_texts = []
            self.license_spdx_codes = []

            self.spdx_dir = os.path.join(
                                os.path.dirname(__file__), 'spdx')
            for file_name in os.listdir(self.spdx_dir):
                if file_name.endswith('.txt'):
                    license_spdx_code = os.path.splitext(file_name)[0]
                    self.license_spdx_codes.append(license_spdx_code)
                    with open(
                            os.path.join(self.spdx_dir, file_name), 'r') as f:
                        license_text = f.read()
                        license_text = self.normilize_text(license_text)
                        self.license_texts.append(license_text)

            self.vectorizer = CountVectorizer(
                                    ngram_range=(1, 3),
                                    stop_words='english')
            X = self.vectorizer.fit_transform(self.license_texts)

            self.classifier = MultinomialNB()
            y = self.license_spdx_codes
            self.classifier.fit(X, y)

            if not os.path.exists(self.cache_dir):
                os.mkdir(self.cache_dir)
            with open(self.cache_file, 'wb') as f:
                pickle.dump((self.vectorizer, self.classifier), f)

    def normilize_text(self, text):
        # remove copyright
        pattern = re.compile(r'(?i)copyright\s+\d{4}(\s*-\s*\d{4})?', re.MULTILINE)
        text = re.sub(pattern, '', text)
        text = text.lower().strip()

        # Remove non-alpha
        text = re.sub('[^0-9a-zA-Z]+', ' ', text)

        # collapse_whitespace
        text = re.sub(' +', ' ', text)

        return text

    def identify_license(self, text):
        text = self.normilize_text(text)
        # text = re.sub('[^0-9a-zA-Z]+', ' ', text)
        X = self.vectorizer.transform([text])
        y = self.classifier.predict(X)
        return y[0], \
            self.classifier.predict_proba(X)[0][
               self.classifier.classes_.tolist().index(y[0])
               ]


class CopyrightIdentifier:
    def __init__(self):
        self.year_range_pattern = re.compile(
                                    r'(\d{4}\s*(?:-|\s+to\s+)\s*\d{4}|\d{4})')

    def identify_year_range(self, text):
        match = re.search(self.year_range_pattern, text)
        if match:
            return match.group(1)
        return None

    def identify_statement(self, text, year_range):
        statement = text.replace(
                        'Copyright',
                        '').replace(year_range, '').strip()
        return statement

    def identify_copyright(self, text):
        lines = text.splitlines()
        for line in lines:
            if 'copyright' in line.lower():
                year_range = self.identify_year_range(line)
                if year_range:
                    statement = self.identify_statement(line, year_range)
                    return year_range, statement
                # else:
                    # statement = self.identify_statement(line, '')
                    # return None, statement
        return None, None


class LicenseAndCopyrightIdentifier:
    def __init__(self):
        self.license_identifier = LicenseIdentifier()
        self.copyright_identifier = CopyrightIdentifier()

    def identify_license(self, text):
        return self.license_identifier.identify_license(text)

    def identify_year_range(self, text):
        return self.copyright_identifier.identify_year_range(text)

    def identify_statement(self, text):
        return self.copyright_identifier.identify_copyright(text)

    def identify_copyright(self, text):
        year_range = self.identify_year_range(text)
        if year_range is None:
            return '', ''
        else:
            statement = self.identify_statement(text)
            return year_range, statement
