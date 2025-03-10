from .schema.SchemaDataset import KeyFamily


class NomisDatasetAnnotations:
    """
    Use our judgement to extract the most useful annotations.
    """

    def __init__(self, keyfamily: KeyFamily):
        tmp = {
            a.annotationtitle: a.annotationtext for a in keyfamily.annotations.annotation
        }
        def getstr(k): return str(tmp.get(k)) if k in tmp else None
        self.status = getstr('Status')
        self.units = getstr('Units')
        self.mnemonic = getstr('Mnemonic')
        self.sources = getstr('contenttype/sources')
        self.subdescription = getstr('SubDescription')
        self.keywords = getstr('Keywords')
        self.metadata_count = getstr('MetadataCount')
        self.geoglevel = getstr('contenttype/geoglevel')
        self.first_released = getstr('FirstReleased')
        self.last_updated = getstr('LastUpdated')
        self.census_release = getstr('contenttype/censusrelease')

    def __str__(self):
        return f"""  [annotations]
    Status: {self.status}
    Units: {self.units}
    Mnemonic: {self.mnemonic}
    Sources: {self.sources}
    SubDescription: {self.subdescription}
    Keywords: {self.keywords}
    MetadataCount: {self.metadata_count}
    Geoglevel: {self.geoglevel}
    FirstReleased: {self.first_released}
    LastUpdated: {self.last_updated}
    CensusRelease: {self.census_release}"""


class NomisDatasetDimensions:
    """
    Extract a tightly structured set of dimensions.
    There are hundreds of single-use dimensions, but we capture those
    which appear in >20% of NOMIS datasets for easy fetching.
    """

    def __init__(self, keyfamily: KeyFamily):
        self.freq = None
        self.measures = None
        self.geo = None
        self.age = None
        self.sex = None
        self.misc = []

        # Always present.
        # eg. "CL_1_1_TIME" or "CL_37_1_TIME"
        self.time = keyfamily.components.timedimension.codelist

        for d in keyfamily.components.dimension:
            if d.isfrequencydimension:
                # All datasets have one frequency dimension
                if self.freq is not None:
                    raise ValueError(f"Duplicate frequency dimensions")
                if d.conceptref != 'FREQ':
                    raise ValueError(f"Frequency dimension is not FREQ")
                self.freq = d.codelist

            elif d.conceptref == 'MEASURES':
                # All datasets have one measures dimension
                if self.measures is not None:
                    raise ValueError(f"Duplicate measures dimensions")
                self.measures = d.codelist

            elif d.conceptref == 'GEOGRAPHY':
                # [1584/1615] datasets have a geography dimension
                if self.geo is not None:
                    raise ValueError(f"Duplicate geography dimensions")
                self.geo = d.codelist

            elif d.conceptref == 'AGE' or d.conceptref == 'C_AGE':
                # 298 datasets have C_AGE
                # 43 datasets have AGE
                if self.age is not None:
                    raise ValueError(f"Duplicate age dimensions")
                self.age = d.codelist

            elif d.conceptref == 'C_SEX' or d.conceptref == 'SEX':
                # 335 datasets have C_SEX
                # 64 datasets have SEX
                if self.sex is not None:
                    raise ValueError(f"Duplicate sex dimensions")
                self.sex = d.codelist

            else:
                # conceptref has very little information to offer beyond this point.
                # Values are like "C_TENHUK11", which isn't descriptive.
                if d.codelist in self.misc:
                    raise ValueError(f"Duplicate dimension {d.codelist}")
                self.misc.append(d.codelist)

    def __str__(self):
        return f"""  [dimensions]
    Freq: {self.freq}
    Measures: {self.measures}
    Geo: {self.geo}
    Age: {self.age}
    Sex: {self.sex}
    Misc: {', '.join(self.misc)}"""


class NomisDataset:
    def __init__(self, keyfamily: KeyFamily):
        # Important!
        self.id = keyfamily.id

        # eg. "Jobseeker's Allowance with rates and proportions"
        self.name = keyfamily.name.value

        # eg. "Records the number of people claiming Jobseeker's..."
        self.description = keyfamily.description.value if keyfamily.description else None

        self.annotations = NomisDatasetAnnotations(keyfamily)
        self.dimensions = NomisDatasetDimensions(keyfamily)

    def __str__(self):
        return f"""[dataset] {self.id}
Name: {self.name}
Description: {self.description}
{self.dimensions}
{self.annotations}"""
