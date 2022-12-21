from marshmallow import Schema, fields


class GeometrySchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)


class AttributesSchema(Schema):
    Measure = fields.Float(required=True)
    OBJECTID = fields.Number()
    Route = fields.Str()
    Measure = fields.Float()
    Distance = fields.Float()
    MMin = fields.Float()
    MMax = fields.Float()


class FeatureSchema(Schema):
    attributes = fields.Dict(required=True)
    geometry = fields.Nested(GeometrySchema)




class MeasureAtPointReturnSchema(Schema):
    displayFieldName = fields.Str()
    fieldAliases = fields.Dict()
    geometryType = fields.Str()
    spatialReference = fields.Dict()
    flds = fields.List(fields.Dict, data_key="fields")
    features = fields.List(fields.Nested(FeatureSchema), required=True)
