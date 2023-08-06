# -*- coding: utf-8 -*-

from datetime import datetime

from cf_units import Unit
import dask.array as da
import numpy as np

from .support import (
    normalize_axis,
    IndexFunction,
    ThresholdMixin,
    ReducerMixin,
    RollingWindowMixin,
    DASK_OPERATORS,
)
from ..util import change_units


class CountLevelCrossings(IndexFunction):
    def __init__(self, threshold):
        super().__init__(units=Unit("1"))
        self.threshold = threshold
        self.extra_coords.append(threshold.copy())

    def prepare(self, input_cubes):
        props = {
            (cube.dtype, cube.units, cube.standard_name)
            for cube in input_cubes.values()
        }
        assert len(props) == 1
        dtype, units, standard_name = props.pop()
        threshold = self.threshold
        threshold.points = threshold.points.astype(dtype)
        if threshold.has_bounds():
            threshold.bounds = threshold.bounds.astype(dtype)
        change_units(threshold, units, standard_name)
        super().prepare(input_cubes)

    def call_func(self, data, axis, **kwargs):
        cond = da.logical_and(
            data["low_data"] < self.threshold.points,
            self.threshold.points < data["high_data"],
        )
        res = np.count_nonzero(cond, axis=axis)
        return res.astype("float32")

    lazy_func = call_func


class CountOccurrences(ThresholdMixin, IndexFunction):
    def __init__(self, threshold, condition):
        super().__init__(threshold, condition, units=Unit("1"))

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        cond = self.condition(data, self.threshold.points)
        res = np.count_nonzero(cond, axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        cond = self.lazy_condition(data, self.threshold.points)
        res = da.count_nonzero(cond, axis=axis)
        return res.astype("float32")


class DiurnalTemperatureRange(ReducerMixin, IndexFunction):
    def __init__(self, statistic="mean"):
        super().__init__(statistic, units=Unit("degree_Celsius"))

    def prepare(self, input_cubes):
        props = {
            (cube.dtype, cube.units, cube.standard_name)
            for cube in input_cubes.values()
        }
        assert len(props) == 1
        dtype, units, standard_name = props.pop()
        assert units.is_convertible(Unit("degree_Celsius"))
        super().prepare(input_cubes)

    def call_func(self, data, axis, **kwargs):
        res = self.reducer(data["high_data"] - data["low_data"], axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        res = self.lazy_reducer(data["high_data"] - data["low_data"], axis=axis)
        return res.astype("float32")


class ExtremeTemperatureRange(IndexFunction):
    def __init__(self):
        super().__init__(units=Unit("degree_Celsius"))

    def prepare(self, input_cubes):
        props = {
            (cube.dtype, cube.units, cube.standard_name)
            for cube in input_cubes.values()
        }
        assert len(props) == 1
        dtype, units, standard_name = props.pop()
        assert units.is_convertible(Unit("degree_Celsius"))
        super().prepare(input_cubes)

    def call_func(self, data, axis, **kwargs):
        res = data["high_data"].max(axis=axis) - data["low_data"].min(axis=axis)
        return res.astype("float32")

    lazy_func = call_func


class FirstOccurrence(ThresholdMixin, IndexFunction):
    def __init__(self, threshold, condition):
        super().__init__(threshold, condition, units=Unit("days"))
        self.NO_OCCURRENCE = np.inf

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        cond = self.condition(data, self.threshold.points)
        res = np.ma.where(
            cond.any(axis=axis), cond.argmax(axis=axis), self.NO_OCCURRENCE
        )
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        cond = self.lazy_condition(data, self.threshold.points)
        res = da.where(cond.any(axis=axis), cond.argmax(axis=axis), self.NO_OCCURRENCE)
        res = da.ma.masked_array(da.ma.getdata(res), mask)
        return res.astype("float32")

    def post_process(self, cube, data, coords, period, **kwargs):
        time = cube.coord("time")
        calendar = time.units.calendar
        offsets = np.empty_like(time.points, dtype=data.dtype)
        for i, representative_date in enumerate(time.cells()):
            year = representative_date.point.year
            start_date = datetime(year, period.first_month_number, 1)
            units = Unit(f"days since {year}-01-01", calendar=calendar)
            offsets[i] = units.date2num(start_date)
        result_data = data + offsets[:, None, None]
        return cube, result_data


class InterdayDiurnalTemperatureRange(IndexFunction):
    def __init__(self):
        super().__init__(units=Unit("degree_Celsius"))

    def prepare(self, input_cubes):
        props = {
            (cube.dtype, cube.units, cube.standard_name)
            for cube in input_cubes.values()
        }
        assert len(props) == 1
        dtype, units, standard_name = props.pop()
        assert units.is_convertible(Unit("degree_Celsius"))
        super().prepare(input_cubes)

    def call_func(self, data, axis, **kwargs):
        res = np.absolute(
            np.diff(data["high_data"] - data["low_data"], axis=axis)
        ).mean(axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        res = da.absolute(
            da.diff(data["high_data"] - data["low_data"], axis=axis)
        ).mean(axis=axis)
        return res.astype("float32")


class LastOccurrence(ThresholdMixin, IndexFunction):
    def __init__(self, threshold, condition):
        super().__init__(threshold, condition, units=Unit("days"))
        self.NO_OCCURRENCE = -np.inf

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        cond = self.condition(np.flip(data, axis=axis), self.threshold.points)
        ndays = data.shape[axis]
        res = np.ma.where(
            cond.any(axis=axis), ndays - cond.argmax(axis=axis), self.NO_OCCURRENCE
        )
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        cond = self.lazy_condition(da.flip(data, axis), self.threshold.points)
        ndays = data.shape[axis]
        res = da.where(
            cond.any(axis=axis), ndays - cond.argmax(axis=axis), self.NO_OCCURRENCE
        )
        res = da.ma.masked_array(da.ma.getdata(res), mask)
        return res.astype("float32")

    def post_process(self, cube, data, coords, period, **kwargs):
        time = cube.coord("time")
        calendar = time.units.calendar
        offsets = np.empty_like(time.points, dtype=data.dtype)
        for i, representative_date in enumerate(time.cells()):
            year = representative_date.point.year
            start_date = datetime(year, period.first_month_number, 1)
            units = Unit(f"days since {year}-01-01", calendar=calendar)
            offsets[i] = units.date2num(start_date)
        result_data = data + offsets[:, None, None]
        return cube, result_data


class Percentile(IndexFunction):
    def __init__(self, percentiles, interpolation="linear"):
        super().__init__(units=Unit("days"))
        points = percentiles.points
        assert np.all(points > 0)
        assert np.all(points < 100)
        self.percentiles = percentiles
        self.interpolation = interpolation
        self.units = "%"

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        self.units = ref_cube.units

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        res = np.percentile(
            data, q=self.percentiles, axis=axis, interpolation=self.interpolation
        )
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)

        def percentile(arr):
            return np.percentile(
                arr, q=self.percentiles.points, interpolation=self.interpolation
            )

        res = da.apply_along_axis(percentile, axis=axis, arr=data).squeeze()
        return res.astype("float32")


class Statistics(ReducerMixin, IndexFunction):
    def __init__(self, statistic):
        super().__init__(statistic)

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        self.units = ref_cube.units

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        res = self.reducer(data, axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        res = self.lazy_reducer(data, axis=axis)
        return res.astype("float32")


class ThresholdedPercentile(ThresholdMixin, IndexFunction):
    def __init__(self, threshold, condition, percentiles, interpolation="linear"):
        super().__init__(threshold, condition)
        points = percentiles.points
        assert np.all(points > 0)
        assert np.all(points < 100)
        self.percentiles = percentiles
        self.interpolation = interpolation

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        self.units = ref_cube.units

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = np.ma.getmaskarray(data).any(axis=axis)
        comb = self.condition(data, self.threshold.points)
        res = np.percentile(
            np.ma.masked_where(~comb, data),
            q=self.percentiles.points,
            axis=axis,
            interpolation=self.interpolation,
        )
        res = np.ma.masked_array(da.ma.getdata(res), mask)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        comb = self.condition(data, self.threshold.points)

        def percentile(arr):
            return np.percentile(
                arr, q=self.percentiles.points, interpolation=self.interpolation
            )

        res = da.apply_along_axis(
            percentile, axis=axis, arr=np.ma.masked_where(~comb, data)
        ).squeeze()
        res = da.ma.masked_array(da.ma.getdata(res), mask)
        return res.astype("float32")


class ThresholdedStatistics(ThresholdMixin, ReducerMixin, IndexFunction):
    def __init__(self, threshold, condition, statistic):
        super().__init__(threshold, condition, statistic, units=Unit("days"))

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        self.units = ref_cube.units

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        comb = self.condition(data, self.threshold.points)
        res = self.reducer(np.ma.masked_where(~comb, data), axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        comb = self.lazy_condition(data, self.threshold.points)
        res = self.lazy_reducer(da.ma.masked_where(~comb, data), axis=axis)
        return res.astype("float32")


class RunningStatistics(RollingWindowMixin, IndexFunction):
    def __init__(self, rolling_aggregator, window_size, overall_statistic):
        super().__init__(rolling_aggregator, window_size, overall_statistic)
        self.fuse_periods = True
        self.bandwidth = self.window_size.points[0] // 2
        self.tail_overlap = self.window_size.points[0] - 1
        self.head_overlap = self.tail_overlap + self.window_size.points[0] % 2

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        self.units = ref_cube.units

    def pre_aggregate_shape(self, *args, **kwargs):
        return (self.head_overlap + self.tail_overlap + 1,)

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = np.ma.getmaskarray(data).any(axis=axis)
        rolling_view = np.lib.stride_tricks.sliding_window_view(
            data, self.window_size.points, axis
        )
        aggregated = self.rolling_aggregator(rolling_view, -1)
        reduced = self.reducer(aggregated, axis=axis)
        masked = np.ma.masked_array(np.ma.getdata(reduced), mask)
        head_slices = (slice(None, None),) * axis + (slice(None, self.head_overlap),)
        head = np.moveaxis(data[head_slices], axis, -1)
        tail_slices = (slice(None, None),) * axis + (slice(-self.tail_overlap, None),)
        tail = np.moveaxis(data[tail_slices], axis, -1)
        res = np.concatenate([head, masked[..., np.newaxis], tail], axis=-1)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        rolling_view = da.overlap.sliding_window_view(
            data, self.window_size.points, axis
        )
        aggregated = self.lazy_rolling_aggregator(rolling_view, -1)
        reduced = self.lazy_reducer(aggregated, axis=axis)
        masked = da.ma.masked_array(da.ma.getdata(reduced), mask)
        head_slices = (slice(None, None),) * axis + (slice(None, self.head_overlap),)
        head = np.moveaxis(data[head_slices], axis, -1)
        tail_slices = (slice(None, None),) * axis + (slice(-self.tail_overlap, None),)
        tail = np.moveaxis(data[tail_slices], axis, -1)
        res = da.concatenate([head, masked[..., np.newaxis], tail], axis=-1)
        return res.astype("float32")

    def post_process(self, cube, data, coords, period, **kwargs):
        def fuse(this, previous_tail, next_head):
            head = this[..., : self.head_overlap]
            pre_statistic = this[..., self.head_overlap]
            tail = this[..., -self.tail_overlap :].copy()
            head_overlap = np.concatenate(
                [previous_tail[..., -self.bandwidth :], head], axis=-1
            )
            head_rolling_view = np.lib.stride_tricks.sliding_window_view(
                head_overlap, self.window_size.points, -1
            )
            head_aggregated = self.lazy_rolling_aggregator(head_rolling_view, axis=-1)
            tail_overlap = np.concatenate(
                [tail, next_head[..., : self.bandwidth]], axis=-1
            )
            tail_rolling_view = np.lib.stride_tricks.sliding_window_view(
                tail_overlap, self.window_size.points, -1
            )
            tail_aggregated = self.lazy_rolling_aggregator(tail_rolling_view, axis=-1)
            concatenated = np.concatenate(
                [head_aggregated, pre_statistic[..., np.newaxis], tail_aggregated],
                axis=-1,
            )
            running_statistic = self.lazy_reducer(concatenated, axis=-1)
            return running_statistic, tail

        if self.fuse_periods and len(data) > 1:
            stack = []
            this = data[0]
            tail_shape = this.shape[:-1] + (self.tail_overlap,)
            previous_tail = da.ma.masked_array(
                da.zeros(tail_shape, dtype=np.float32),
                False,
            )

            for next_chunk in data[1:]:
                next_head = next_chunk[..., : self.head_overlap].copy()
                running_statistic, previous_tail = fuse(this, previous_tail, next_head)
                stack.append(running_statistic)
                this = next_chunk

            head_shape = this.shape[:-1] + (self.head_overlap,)
            next_head = da.ma.masked_array(
                da.zeros(head_shape, dtype=np.float32),
                False,
            )

            stack.append(fuse(next_chunk, previous_tail, next_head)[0])
            res_data = da.stack(stack, axis=0)
        else:
            res_data = self.lazy_reducer(data[..., 1:], axis=-1)
        return cube, res_data


class ThresholdedRunningStatistics(ThresholdMixin, RunningStatistics):
    def __init__(
        self, threshold, condition, rolling_aggregator, window_size, overall_statistic
    ):
        super().__init__(
            threshold, condition, rolling_aggregator, window_size, overall_statistic
        )

    def call_func(self, data, axis, **kwargs):
        comb = self.condition(data, self.threshold.points)
        thresholded_data = np.where(comb, data, 0.0)
        return super().call_func(thresholded_data, axis, **kwargs)

    def lazy_func(self, data, axis, **kwargs):
        comb = self.condition(data, self.threshold.points)
        thresholded_data = da.ma.where(comb, data, 0.0)
        return super().lazy_func(thresholded_data, axis, **kwargs)


class TemperatureSum(ThresholdMixin, IndexFunction):
    def __init__(self, threshold, condition):
        super().__init__(threshold, condition, units=Unit("days"))
        if condition in [">", ">="]:
            self.fun = lambda d, t: np.maximum(d - t, 0)
            self.lazy_fun = lambda d, t: da.maximum(d - t, 0)
        else:
            self.fun = lambda d, t: np.maximum(t - d, 0)
            self.lazy_fun = lambda d, t: da.maximum(t - d, 0)

    def prepare(self, input_cubes):
        super().prepare(input_cubes)
        ref_cube = next(iter(input_cubes.values()))
        self.standard_name = ref_cube.standard_name
        if ref_cube.units.is_convertible("degC"):
            self.units = "degC days"
        else:
            raise RuntimeError("Invalid input units")

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        threshold = self.threshold.points[0]
        res = np.sum(self.fun(data, threshold), axis=axis)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        threshold = self.threshold.points[0]
        res = da.sum(self.lazy_fun(data, threshold), axis=axis)
        return res.astype("float32")


class CountJointOccurrences(IndexFunction):
    def __init__(self, mapping):
        super().__init__(units=Unit("1"))
        self.mapping = mapping

    def add_extra_coords(self, input_cubes):
        thresholds = []
        for name, _ in input_cubes.items():
            for threshold, _ in self.mapping[name]:
                thresholds.append(threshold)
        if (
            thresholds[0].metadata.equal(thresholds[1].metadata, lenient=True)
            and thresholds[0].metadata.long_name == thresholds[1].metadata.long_name
        ):
            raise ValueError(
                "Auxiliary coordinates with the same metadata must have different "
                "<long_name>."
            )
        self.extra_coords.append(thresholds[0].copy())
        self.extra_coords.append(thresholds[1].copy())

    def prepare(self, input_cubes):
        self.add_extra_coords(input_cubes)
        props = {
            (name, cube.dtype, cube.units, cube.standard_name)
            for name, cube in input_cubes.items()
        }
        for (data_name, dtype, units, standard_name) in props:
            for threshold, _ in self.mapping[data_name]:
                threshold.points = threshold.points.astype(dtype)
                if threshold.has_bounds():
                    threshold.bounds = threshold.bounds.astype(dtype)
                change_units(threshold, units, standard_name)
        super().prepare(input_cubes)

    def lazy_func(self, data, axis, **kwargs):
        if not isinstance(data, dict):
            data = {"data": data}
        conditions = []
        for name, arr in data.items():
            for threshold, operator in self.mapping[name]:
                conditions.append(operator(arr, threshold.points))
        cond = da.all(da.stack(conditions, axis=0), axis=0)
        res = da.count_nonzero(cond, axis=axis)
        return res.astype("float32")

    call_func = lazy_func


class CountJointOccurrencesPrecipitationTemperature(CountJointOccurrences):
    def __init__(
        self,
        threshold_precip_data,
        threshold_temp_data,
        condition_precip_data,
        condition_temp_data,
    ):
        super().__init__(
            mapping={
                "precip_data": [
                    (threshold_precip_data, DASK_OPERATORS[condition_precip_data])
                ],
                "temp_data": [
                    (threshold_temp_data, DASK_OPERATORS[condition_temp_data])
                ],
            }
        )


class CountJointOccurrencesTemperature(CountJointOccurrences):
    def __init__(
        self,
        threshold_low_data,
        threshold_high_data,
        condition_low_data,
        condition_high_data,
    ):
        super().__init__(
            mapping={
                "data": [
                    (threshold_low_data, DASK_OPERATORS[condition_low_data]),
                    (threshold_high_data, DASK_OPERATORS[condition_high_data]),
                ]
            }
        )
