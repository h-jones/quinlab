classdef (ConstructOnLoad = true) lfm < handle
    properties (Access = public)
        automation;
        addinbase;
        application;
        experiment;
    end
    methods
        function out = lfm(visible)
            out.addinbase = PrincetonInstruments.LightField.AddIns.AddInBase();
            out.automation = PrincetonInstruments.LightField.Automation.Automation(visible,[]);
            out.application = out.automation.LightFieldApplication;
            out.experiment = out.application.Experiment;
            
        end
    	function close(obj)
			obj.automation.Dispose();
        end
        function set(obj,setting,value)
            if obj.experiment.Exists(setting)
                if obj.experiment.IsValid(setting,value)
                    obj.experiment.SetValue(setting,value);
                end
            end
        end
        function return_value = get(obj,setting)
            if obj.experiment.Exists(setting)
                return_value = obj.experiment.GetValue(setting);
            end
        end
        function load_experiment(obj,value)
            obj.experiment.Load(value);
        end
        function set_exposure(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.ShutterTimingExposureTime,value);
        end
        function return_value = get_exposure(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.ShutterTimingExposureTime);
        end
        function set_frames(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FrameSettingsFramesToStore,value);
        end
        function return_value = get_frames(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FrameSettingsFramesToStore);
        end
        function set_adcquality(obj,value)
        % 1 LowNoise or 2 HighCapacity
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcQuality,value)
        end
        function return_value = get_adcquality(obj)
            return_value = int8(double(obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcQuality)));
        end
        function set_adcspeed(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcSpeed,value);
        end
        function return_value = get_adcspeed(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcSpeed);
        end
        function set_adcanaloggain(obj,value)
        % 1 Low, 2 Medium, 3 High
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcAnalogGain,value)
        end
        function return_value = get_adcanaloggain(obj)
            return_value = int8(double(obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcAnalogGain)));
        end
        function return_value = get_adcbitdepth(obj,value)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.AdcBitDepth);
        end
        function set_binwidth(obj,value)
        % 1 - 1340
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestBinnedSensorXBinning,value);
        end
        function return_value = get_binwidth(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestBinnedSensorXBinning);
        end
        function set_binheight(obj,value)
        % 1 - 400
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestBinnedSensorYBinning,value);
        end
        function return_value = get_binheight(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestBinnedSensorYBinning);
        end
        function set_roiselection(obj,value)
        % 1 FullSensor, 2 BinnedSensor, 3 LineSensor, 4 CustomRegions
            obj.set(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestSelection,value)
        end
        function return_value = get_roiselection(obj)
            return_value = int8(double(obj.get(PrincetonInstruments.LightField.AddIns.CameraSettings.ReadoutControlRegionsOfInterestSelection)));
        end
        function set_grating(obj,value)
            if value == 300
                obj.set(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.GratingSelected,'[1umum,300][2][0]');
            elseif value == 1200
                obj.set(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.GratingSelected,'[750nm,1200][1][0]');
            elseif value == 1800
                obj.set(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.GratingSelected,'[500nm,1800][0][0]');
            end
        end
        function set_centerwavelength(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.GratingCenterWavelength,value);
        end
        function return_value = get_centerwavelength(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.GratingCenterWavelength);
        end
        function set_slitwidth(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.OpticalPortEntranceFrontWidth,value);
        end
        function return_value = get_slitwidth(obj)
            return_value = obj.get(PrincetonInstruments.LightField.AddIns.SpectrometerSettings.OpticalPortEntranceFrontWidth);
        end
        function set_filename(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FileNameGenerationBaseFileName,value)
        end
        function set_directory(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FileNameGenerationDirectory,value)
        end
        function set_filedate(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FileNameGenerationAttachDate,value)
        end
        function set_filetime(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FileNameGenerationAttachTime,value)
        end
        function set_fileincrement(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.FileNameGenerationAttachIncrement,value)
        end
        function set_export(obj,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.OnlineExportEnabled,value)
            obj.set(PrincetonInstruments.LightField.AddIns.ExperimentSettings.OnlineExportFormatOptionsIncludeExperimentInformation,true)
        end
        function acquire(obj,timeout)
            while obj.experiment.IsRunning
            end
            obj.experiment.Acquire();
            t0 = clock;
            while obj.experiment.IsRunning
                if etime(clock,t0) > timeout
                    obj.experiment.Stop();
                    acquire(obj,timeout);
                    break;
                end
            end
        end
    end
end


